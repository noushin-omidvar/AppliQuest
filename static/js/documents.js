const user_id = localStorage.getItem("user_id");

// Delete button click event handler
$(".delete-document").on("click", async function (e) {
  $(this).closest(".document-card").remove();
  const documentItem = e.target.closest(".document-card");
  const documentId = documentItem.dataset.documentid;
  await axios.delete(`/api/v1/users/${user_id}/documents/${documentId}`);
});

// // Edit button click event handler
// $(".edit-document").on("click", async function (e) {
//   const documentItem = e.target.closest(".document-card");
//   const documentId = documentItem.dataset.documentid;
//   console.log(documentId);
//   $("#detailDocumentModal").modal("show");
//   document_resp = await axios.get(
//     `/api/v1/users/${user_id}/documents/${documentId}`
//   );
//   document_data = document_resp.data;
//   $("#detail_document_form [name='title']").val(document_data.document.title);
//   $("#detail_document_form [name='category']").val(
//     document_data.document.category
//   );

//   console.log(document_data.document.file);
//   const PDFStart = (nameRoute) => {};
//   const startPdf = () => {
//     PDFStart(document_data.document.file);
//   };
//   window.addEventListener("load", startPdf);
//   let loadingTask = pdfjsLib.getDocument(nameRoute),
//     pdfDoc = null,
//     canvas = document.querySelector("#cnv"),
//     ctx = canvas.getContext("2d"),
//     scale = 1.5,
//     numPage = 1;

//   loadingTask.promise.then((pdfDoc_) => {
//     pdfDoc = pdfDoc_;
//     document.querySelector("#npages").innerHTML = pdfDoc.numPages;
//     GeneratePDF(numPage);
//   });

//   const GeneratePDF = (numPage) => {
//     pdfDoc.getPage(numPage).then((page) => {
//       let viewport = page.getViewport({ scale: scale });
//       canvas.height = viewport.height;
//       canvas.width = viewport.width;
//       let renderContext = {
//         canvasContext: ctx,
//         viewport: viewport,
//       };
//       page.render(renderContext);
//     });
//     document.querySelector("#npages").innerHTML = numPage;
//   };
// });
// // Create new document
// $("button#create-document.btn").on("click", async function (e) {
//   const formData = new FormData();
//   formData.append("file_to_save", $("#file-to-save")[0].files[0]);
//   formData.append("category", $("#category").val());
//   formData.append("file_name", $("#file-name").val());

//   await axios.post(`/api/v1/users/${user_id}/documents`, formData, {
//     headers: {
//       "Content-Type": "multipart/form-data",
//     },
//   });

//   console.log("posted");
//   $("#newDocumentModal").modal("hide");
//   location.reload();
// });

//   $("button#create-document").on("click", async function (e) {
//     await axios.patch(`/api/v1/users/${user_id}/documents/${documentId}`, {
//       first_name: $("#new_document_form [name='first_name']").val(),
//       last_name: $("#new_document_form [name='last_name']").val(),
//       company: document_data.document.company,
//       email: $("#new_document_form [name='email']").val(),
//       phone: $("#new_document_form [name='phone']").val(),
//       notes: $("#new_document_form [name='notes']").val(),
//     });
//     $("#detailDocumentModal").modal("hide");
//     location.reload();
//   });
// });

// Add event listener to edit button
$(".edit-document").on("click", async function (e) {
  const documentId = $(this).closest(".document-card").data("documentid");

  const response = await axios.get(`/api/v1/documents/${documentId}/file`);
  const fileUrl = response.data;

  // Create an <iframe> element
  const iframe = document.createElement("iframe");
  iframe.src = fileUrl;
  iframe.width = "100%";
  iframe.height = "100%";
  iframe.style.border = "none";

  // Create a <div> element for the modal body
  const modalBody = document.querySelector("#file-display");
  modalBody.innerHTML = "";
  modalBody.appendChild(iframe);

  // Open modal and display the file
  $("#detailDocumentModal").modal("show");
});

function openModalWithFile(fileUrl) {
  // Create an <iframe> element
  const iframe = document.createElement("iframe");
  iframe.src = fileUrl;
  iframe.style.width = "100%";
  iframe.style.height = "100%";

  // Add the <iframe> to the modal body
  const modalBody = document.querySelector("#file-display");
  modalBody.innerHTML = "";
  modalBody.appendChild(iframe);

  // Open the modal
  $("#detailDocumentModal").modal("show");
}
