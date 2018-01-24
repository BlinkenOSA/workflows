# Pipline for creating and preserving an AIP from a master video:
	1. Create a directory stucture		
		- Make top level directory: BARCODE
			- Make CONTENT directory
			- Make METADATA directory
	2. Copy the ffv1 file to the CONTENT directory		
		- with RSYNC >> checksum on the fly
	3. Create technical metadata
		- mediainfo & ffprobe
		- push into METADATA directory
	4. Push techical metadata to AMS
	5. {Pull descriptive metadata from AMS}
	6. Generate access copy
	7. Copy access copy to destination
	8. Send email to AV and IT
