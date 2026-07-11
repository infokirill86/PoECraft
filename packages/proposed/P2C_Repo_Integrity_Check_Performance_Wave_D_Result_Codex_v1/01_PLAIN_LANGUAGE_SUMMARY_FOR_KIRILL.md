# Plain-Language Summary for Kirill

The old checksum tools started Git separately for every repository file. With hundreds of files, almost all elapsed time was process startup rather than hashing.

The new implementation asks Git for every tracked file through one continuous batch stream per tool. It still checks every file and still hashes Git-normalized index bytes. The root manifest before and after has the same SHA-256, so the acceleration did not change its contents.

Measured on this clone, update fell from about 57 seconds to well under one second, and verification fell from about 57 seconds to well under one second. Exact timings are evidence, not a permanent performance guarantee across machines.

Wave D remains proposed until Claude audits it and ChatGPT/User accepts it.
