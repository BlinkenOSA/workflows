# av-preservation-workflow
DAG definitions for the various workflows at Blinken OSA Archivum.

## Requirements
Runs on Docker, so the only prerequisite is to install Docker to your system.

## Launch
+ Clone the repository
+ Run the `start-airflow.sh` script which compiles and runs the necessary Docker containers.

## Workflows
### osa-av-workflow
Worflow for handling the digitized files of the analogue cassettes (VHS, BETA) and create Archival Information Packages.

#### Workflow steps
The workflow is defined in as a DAG, which recursively calls itself until there are files to be processed. The files for
this DAG are in the directory `dags\av_tasks`:

1. `collect_files.py` - Picking up the next file to process. The file should be named according to the barcode pattern
(with the predefined extension), or should be in a directory which has the same pattern as the barcode.
2. `create_directories.py` - Creating the target directory structure for the Archival Information Package.
The structure of the Archival Information Package is the following:

```bash
.
└── HU_OSA_00000001
    ├── Content
    │   ├── Access
    │       └── HU_OSA_00000001.mp4
    │   └── Preservation
    │       └── HU_OSA_00000001.mpg
    └── Metadata
        ├── Access
            ├── HU_OSA_00000001.md5
            ├── HU_OSA_00000001.sha512
            └── HU_OSA_00000001_md_tech.json
        └── Preservation
            ├── HU_OSA_00000001.md5
            ├── HU_OSA_00000001.sha512
            ├── HU_OSA_00000001_md_descriptive.json
            └── HU_OSA_00000001_md_tech.json

```

3. `copy_master_files.py` - Moves the master files to their respective directory under
`AIP/Content/Preservation`
4. `create_checksums.py` - Creates checksum for the master file using md5 and sha512 algorithms.
5. `create_video_info.py` - Using `ffprobe` technical metadata is created for the master file, under
`AIP/Metadata/Preservation/<Barcode>_md_tech.json`
6. `get_decriptive_metadata.py` - Fetches the descriptive metadata from the Archival Management System
if exists.
7. `push_to_ams.py` - Using the barcode, the technical metadata is pushed to OSAs Archival Management System,
and the `digital_version_exists` flag is set.
8. `encode_masters.py` - Using `ffmpeg` high-quality access copies are created under:
`AIP/Content/Access`
9. `create_checksums.py` - Creates checksum for the access copy file using md5 and sha512 algorithms.
10. `create_video_info.py` - Using `ffprobe` technical metadata is created for the master file, under
`AIP/Metadata/Access/<Barcode>_md_tech.json
11. `send_email.py` - Sending an email to the staff members of the AV digitization procedure.

#### Settings
To be able to pick up source and target locations, and various settings, the following settings should be made
in `docker-compose.yml`
##### Volumes
+ A directory containing source files should be mapped to `/opt/input`
+ A directory containing target files should be mapped to `/opt/output`
##### Environment variables
###### AMS Specific
+ `AMS_API` - The URL of the API of the Archival Management System
+ `AMS_API_TOKEN` - The API token of the Archival Management System
###### Workflow Specific
+ `AV_FINAL_DIR` - Directory of the target files
+ `AV_MASTER_FILE_EXTENSION` - File extension of the source files
+ `AV_ACCESS_FILE_EXTENSION` - File extension of the access files
+ `AV_BARCODE_PATTERN` - Regexp pattern of the barcodes registered
+ `AV_STAFF_EMAIL_LIST` - Comma separated list of the AV Staff email addresses