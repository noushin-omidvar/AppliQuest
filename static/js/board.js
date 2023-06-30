/** Get user_id from the serverside */
function get_user_id() {
  userId = localStorage.getItem("user_id");
  return userId;
}

async function main() {
  /** Implementing the drag and drop of Kanban items */
  dragula([
    document.querySelector("#Wishlist"),
    document.querySelector("#Applied"),
    document.querySelector("#Interview"),
    document.querySelector("#Offer"),
    document.querySelector("#Rejected"),
  ]).on("drop", async function (el, target, source, sibling) {
    user_id = localStorage.getItem("user_id");
    job_id = el.dataset.job_id;
    today = new Date();

    resp = await axios.get(`/api/v1/users/${user_id}/jobs/${job_id}`);

    const formattedDate = today
      .toUTCString()
      .replace(/\d{2}:\d{2}:\d{2}/, "00:00:00");
    await axios.patch(`/api/v1/users/${user_id}/jobs/${job_id}`, {
      status: target.id,
      modified_at: formattedDate,
    });
    location.reload();
  });

  function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
    let currentFocus;

    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function (e) {
      let a,
        b,
        i,
        val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) {
        return false;
      }
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
          b.addEventListener("click", function (e) {
            /*insert the value for the autocomplete text field:*/
            inp.value = this.getElementsByTagName("input")[0].value;
            /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
            closeAllLists();
          });
          a.appendChild(b);
        }
      }
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function (e) {
      let x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) {
        //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
    });
    function addActive(x) {
      /*a function to classify an item as "active":*/
      if (!x) return false;
      /*start by removing the "active" class on all items:*/
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = x.length - 1;
      /*add class "autocomplete-active":*/
      x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
      /*a function to remove the "active" class from all autocomplete items:*/
      for (let i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
      }
    }
    function closeAllLists(elmnt) {
      /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
      let x = document.getElementsByClassName("autocomplete-items");
      for (let i = 0; i < x.length; i++) {
        if (elmnt != x[i] && elmnt != inp) {
          x[i].parentNode.removeChild(x[i]);
        }
      }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
      closeAllLists(e.target);
    });
  }

  $("#newJobModal").ready(function () {
    $("#company_name").on("input", async function () {
      let query = $(this).val();

      if (query.length >= 2) {
        resp = await axios.post("/api/v1/companies/autocomplete_company", {
          query: query,
        });
        autocomplete(document.getElementById("company_name"), resp.data);
      }
    });
  });

  $(document).on("click", "#create-job", async function (e) {
    e.preventDefault();
    user_id = localStorage.getItem("user_id");
    const resp = await axios.get("/api/v1/companies");
    let companies = resp.data["companies"];
    let company_dict = {};
    for (let i = 0; i < companies.length; i++) {
      company_dict[companies[i]["company_name"]] = companies[i]["id"];
    }

    let job_title = $("#job_title").val();
    let company_name = $("#company_name").val();
    let status = $("#status").val();

    console.log(company_name);
    console.log(Object.keys(company_dict));

    if (!(company_name in Object.keys(company_dict))) {
      let resp = await axios.post("/api/v1/companies", {
        company_name: company_name,
      });
      company = resp.data["new_company"];
    } else {
      resp = await axios.get(`/api/v1/companies/${company_dict[company_name]}`);
      company = resp.data["company"];
    }
    resp_job = await axios.post(`/api/v1/users/${user_id}/jobs`, {
      job_title: job_title,
      company: company,
      status: status,
    });
    job_id = resp_job.data["id"];
    $("#new_job_form")[0].reset();
    $("#newJobModal").modal("hide");
    $("#" + status).append(
      `<div
    class="card mb-3 cursor-grab job-card text-light flex-row"
    data-job_title=${job_title}
    data-job_id=${job_id}
    data-user_id=${user_id}}
  >
    <div
      class="p-2 mx-2 mt-3 bg-light rounded-circle overflow"
      style="width: 50px; height: 50px"
    >
      <img
        src="/static/images/building.png"
        class="card-img-left float-left"
        width="50px"
        height="auto"
      />
    </div>
    <div class="card-body text-truncate">
    <b>${job_title}</b>
    <p class="mb-0">${company_name}</p>


    <small>Today</small>
  </div>

  <div class="float-left me-3 mt-3">
    <p>
      <i
        class="fa-regular fa-trash-can delete-job border border-light rounded p-1 job-icon"
      ></i>
    </p>
    <p class="fs-6">
      <i
        class="fa-solid fa-link fa-sm link-job border border-light rounded job-icon"
      ></i>
    </p>
  </div>
</div>`
    );
  });

  //SHow job detail form
  $(document).on("click", ".job-card", async function (e) {
    e.preventDefault();
    console.log($(e.target));

    // user_id = localStorage.getItem("user_id");

    job_id = e.target.closest(".job-card").dataset.job_id;
    localStorage.setItem("job_id", job_id);
    job_resp = await axios.get(`/api/v1/users/${user_id}/jobs/${job_id}`);
    job_data = job_resp.data;
    $("#job-form [name='job_title']").val(job_data.job.job_title);
    company_id = job_data.job.company_id;

    company_resp = await axios.get(`/api/v1/companies/${company_id}`);
    company_data = company_resp.data;
    $("#job-form [name='company_name']").val(company_data.company.company_name);
    $("#job-form [name='status']").val(job_data.job.status);
    $("#job-form [name='post_url']").val(job_data.job.post_url);
    $("#job-form [name='job_location']").val(job_data.job.job_location);
    $("#job-form [name='notes']").val(job_data.job.notes);
    $("#job-form [name='job_description']").val(job_data.job.job_description);

    if ($(e.target).hasClass("link-job")) {
      window.open(job_data.job.post_url);
      return;
    } else if ($(e.target).hasClass("delete-job")) {
      console.log(e.target);
      resp_del = await axios.delete(`/api/v1/users/${user_id}/jobs/${job_id}`);
      e.target.closest(".job-card").remove();
      return;
    }

    $("#JobDetailModal").modal("show");
  });

  //save changes to job from detail form
  $(document).on("click", "#save-job", async function (e) {
    e.preventDefault();

    user_id = localStorage.getItem("user_id");
    job_id = localStorage.getItem("job_id");
    const resp = await axios.get("/api/v1/companies");
    let companies = resp.data["companies"];
    let company_dict = {};
    for (let i = 0; i < companies.length; i++) {
      company_dict[companies[i]["company_name"]] = companies[i]["id"];
    }

    let job_title = $("#job_title").val();
    let company_name = $("#company_name").val();
    let status = $("#status").val();

    if (!(company_name in Object.keys(company_dict))) {
      let resp = await axios.post("/api/v1/companies", {
        company_name: company_name,
      });
      company = resp.data["new_company"];
    } else {
      resp = await axios.get(`/api/v1/companies/${company_dict[company_name]}`);
      company = resp.data["company"];
    }
    await axios.patch(`/api/v1/users/${user_id}/jobs/${job_id}`, {
      job_title: job_title,
      company: company,
      status: status,
      post_url: post_url,
      job_location: job_location,
      note: notes,
      job_description: job_description,
    });
    $("#JobDetailModal").modal("hide");
    localStorage.removeItem("job_id");
  });
}

main();
