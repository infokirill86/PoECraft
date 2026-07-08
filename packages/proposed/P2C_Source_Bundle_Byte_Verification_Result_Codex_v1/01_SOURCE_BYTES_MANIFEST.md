# Source Bytes Manifest

See `SOURCE_BYTES_MANIFEST.csv` for machine-readable source file SHA256 values.

Included source bytes are copied into `SOURCE_BYTES/` because this package is explicitly a SOURCE_BUNDLE / byte-verification result, not an ordinary delta.

Historical audit Markdown files are recorded in `SOURCE_BYTES_MANIFEST.csv` as reference metadata only. Their bytes are not included in `SOURCE_BYTES/` because this bundle is focused on prior baseline ZIP package bytes, and the audit text is not the imported runtime/data source tree.

Missing source bytes are documented as gaps, not invented.
