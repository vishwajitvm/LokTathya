# OCR Policy
OCR is strictly a fallback. We extract native text first. If text density/quality falls below threshold, we enqueue Tesseract/LayoutLM OCR jobs.
