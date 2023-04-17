user_id = '<%= Session["curr_user"] %>';
console.log(user_id);
dragula([
  document.querySelector("#Wishlist"),
  document.querySelector("#Applied"),
  document.querySelector("#Interview"),
  document.querySelector("#Offer"),
  document.querySelector("#Rejected"),
]).on("drop", async function (el, target, source, sibling) {
  console.log(target);
  console.log(source);
  user_id = el.dataset.user_id;
  job_id = el.dataset.job_id;

  await axios.patch(`/api/users/${user_id}/jobs/${job_id}`, {
    status: target.id,
  });
});

$;
