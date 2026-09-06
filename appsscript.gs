function doGet(e) {
  const q = e.parameter.q || "";
  const tl = e.parameter.tl || "ca";
  if (!q) {
    return ContentService.createTextOutput("").setMimeType(ContentService.MimeType.TEXT);
  }
  const out = LanguageApp.translate(q, "auto", tl);
  return ContentService.createTextOutput(out).setMimeType(ContentService.MimeType.TEXT);
}