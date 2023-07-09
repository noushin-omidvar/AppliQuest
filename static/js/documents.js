// Delete button click event handler
$(".delete-document").on("click", async function (e) {
  $(this).closest(".document-card").remove();
  const documentItem = e.target.closest(".document-card");
  const documentId = documentItem.dataset.documentid;
  await axios.delete(`/api/v1/users/${user_id}/documents/${documentId}`);
});

// Create new document
$("button#create-document.btn").on("click", async function (e) {
  const formData = new FormData();
  formData.append("file_to_save", $("#file-to-save")[0].files[0]);
  formData.append("category", $("#category").val());
  formData.append("file_name", $("#file-name").val());

  await axios.post(`/api/v1/users/${user_id}/documents`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  $("#newDocumentModal").modal("hide");
  location.reload();
});

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
