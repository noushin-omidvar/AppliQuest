dragula([
  document.querySelector("#wishlist"),
  document.querySelector("#applied"),
  document.querySelector("#interview"),
  document.querySelector("#offer"),
  document.querySelector("#rejected"),
]).on("drop", function (el, target, source, sibling) {
  console.log(target.id);
  console.log(source.id);
  // $.ajax({
  //   url: `/api/${user_id}/jobs/${job_id}`,
  //   type: 'POST',
  //   data: {
  //     new_status: target.id,
  //     old_status: source.id
  //   }
  // });
});
