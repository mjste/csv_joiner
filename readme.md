# csv_joiner

This program (yet not complete) reads two files and joins them by given column name.

It is assumed that input files may be very large, therefore too large for RAM to handle. My approach first sorts both files by given column reading them as streams. Thata approach is possibly much slower than doing this in RAM, however it needs limited memory, independent of file size.

Then sorted files, are again treated as streams, and join operation is performed.

Current version does not support printing to standard output, only to out file. It was done due to easier debugging in that form. And lack of time.
