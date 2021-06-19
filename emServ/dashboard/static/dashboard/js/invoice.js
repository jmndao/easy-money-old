window.html2canvas = html2canvas;
window.jsPDF = window.jsPDF.jsPDF;
function to_pdf() {
  html2canvas(document.querySelector('#capture'), {
    allowTaint: true,
    useCORS: true,
    scale: 1
  }).then(canvas => {
    var img = canvas.toDataURL('image/png');
    var doc = new jspdf();
    doc.setFont('Arial');
    doc.setFontSize(11);
    doc.addImage(img, 'PNG', 7, 13);
    doc.save('html_to_pdf')

  });
}
