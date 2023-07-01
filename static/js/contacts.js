// const user_id = localStorage.getItem("user_id");

// Delete button click event handler
$(".delete-contact").on("click", async function (e) {
  $(this).closest(".contact-card").remove();
  const contactItem = e.target.closest(".contact-card");
  const contactId = contactItem.dataset.contactid;
  await axios.delete(`/api/v1/users/${user_id}/contacts/${contactId}`);
});

// Edit button click event handler
$(".edit-contact").on("click", async function (e) {
  const contactItem = e.target.closest(".contact-card");
  const contactId = contactItem.dataset.contactid;
  $("#detailContactModal").modal("show");
  contact_resp = await axios.get(
    `/api/v1/users/${user_id}/contacts/${contactId}`
  );
  contact_data = contact_resp.data;
  $("#detail_contact_form [name='first_name']").val(
    contact_data.contact.first_name
  );
  $("#detail_contact_form [name='last_name']").val(
    contact_data.contact.last_name
  );
  $("#detail_contact_form [name='company']").val(contact_data.contact.company);
  $("#detail_contact_form [name='email']").val(contact_data.contact.email);
  $("#detail_contact_form [name='phone']").val(contact_data.contact.phone);
  $("#detail_contact_form [name='notes']").val(contact_data.contact.notes);

  // Creat new contact
  $("button#create-contact").on("click", async function (e) {
    await axios.patch(`/api/v1/users/${user_id}/contacts/${contactId}`, {
      first_name: $("#detail_contact_form [name='first_name']").val(),
      last_name: $("#detail_contact_form [name='last_name']").val(),
      company: contact_data.contact.company,
      email: $("#detail_contact_form [name='email']").val(),
      phone: $("#detail_contact_form [name='phone']").val(),
      notes: $("#detail_contact_form [name='notes']").val(),
    });
    $("#detailContactModal").modal("hide");
    location.reload();
  });
});
