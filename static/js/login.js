// Select the login form using its ID or class
const $loginForm = $("#login-form");
const reme = $("#remember-me");
// Attach a submit event handler to the form
$loginForm.on("submit", function (event) {
  event.preventDefault();
  const formData = $(this).serialize();
  // Make an AJAX request using Axios
  axios
    .post("/login", formData)
    .then(function (response) {
      // Check if login was successful
      if (response.data.hasOwnProperty("user_id")) {
        // Store user ID in local storage
        localStorage.setItem("user_id", response.data.user_id);

        // Redirect to the board page
        window.location.href = "/board";
      } else {
        // Display error message if login failed
        alert(response.data.error);
      }
    })
    .catch(function (error) {
      // Handle any AJAX request error
      console.log("AJAX request failed:", error);
    });
});
