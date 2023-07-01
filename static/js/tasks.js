const user_id = localStorage.getItem("user_id");
$(".form-check-input").on("click", async (e) => {
  const taskItem = e.target.closest(".list-group-item");
  const taskTextElement = taskItem.querySelector(".task-text");
  const taskId = taskItem.dataset.taskId;

  if (e.target.checked) {
    taskTextElement.style.textDecoration = "line-through";
  } else {
    taskTextElement.style.textDecoration = "none";
  }

  await axios.patch(`/api/v1/users/${user_id}/tasks/${taskId}`, {
    completed: e.target.checked,
  });
});

$("#All").on("click", () => location.reload());

$("#Due-Today").on("click", async (e) => {
  $("#tasks-cat").text("Tasks > Due Today");
  $(".list-group").addClass("d-none");
  $("#Due-Today-list").removeClass("d-none");
  $(".on-view").removeClass("on-view");
  $("#Due-Today").addClass("on-view");
});

$("#Past-Due").on("click", async (e) => {
  $("#tasks-cat").text("Tasks > Past Due ");
  $(".list-group").addClass("d-none");
  $("#Past-Due-list").removeClass("d-none");
  $(".on-view").removeClass("on-view");
  $("#Past-Due").addClass("on-view");
});

$("#Completed").on("click", async (e) => {
  $("#tasks-cat").text("Tasks > Completed ");
  $(".list-group").addClass("d-none");
  $("#Completed-list").removeClass("d-none");
  $(".on-view").removeClass("on-view");
  $("#Completed").addClass("on-view");
});

$("#Wishlists").on("click", async (e) => {
  $("#tasks-cat").text("Tasks > Wishlists ");
  $(".list-group").addClass("d-none");
  $("#Wishlists-list").removeClass("d-none");
  $(".on-view").removeClass("on-view");
  $("#Wishlists").addClass("on-view");
});

$("#Applications").on("click", async (e) => {
  $("#tasks-cat").text("Tasks > Applications ");
  $(".list-group").addClass("d-none");
  $("#Applications-list").removeClass("d-none");
  $(".on-view").removeClass("on-view");
  $("#Applications").addClass("on-view");
});

$("#Interviews").on("click", async (e) => {
  $("#tasks-cat").text("Tasks > Interviews ");
  $(".list-group").addClass("d-none");
  $("#Interviews-list").removeClass("d-none");
  $(".on-view").removeClass("on-view");
  $("#Interviews").addClass("on-view");
});

$("#Offers").on("click", async (e) => {
  $("#tasks-cat").text("Tasks > Offers ");
  $(".list-group").addClass("d-none");
  $("#Offers-list").removeClass("d-none");
  $(".on-view").removeClass("on-view");
  $("#Offers").addClass("on-view");
});

$("#Rejections").on("click", async (e) => {
  $("#tasks-cat").text("Tasks > Rejections ");
  $(".list-group").addClass("d-none");
  $("#Rejections-list").removeClass("d-none");
  $(".on-view").removeClass("on-view");
  $("#Rejections").addClass("on-view");
});

// Edit button click event handler
$(".edit-button").on("click", async function (e) {
  const taskItem = e.target.closest(".list-group-item");
  const taskId = taskItem.dataset.taskId;
  $("#detailTaskModal").modal("show");
  task_resp = await axios.get(`/api/v1/users/${user_id}/tasks/${taskId}`);
  task_data = task_resp.data;
  $("#detail_task_form [name='task']").val(task_data.task.task_title);
  // document.querySelector("#detail_task_form [name='job']").value =
  // task_data.task.job_id;

  $("#detail_task_form [name='startdate']").val(task_data.task.created_at);
  $("#detail_task_form [name='enddate']").val(task_data.task.due_date);
  $("#detail_task_form [name='notes']").val(task_data.task.notes);
  $("#detail_task_form [name='completed']").val(task_data.task.completed);

  // Creat new task
  $("button#create-task").on("click", async function (e) {
    console.log(e.target);
    console.log("hi");
    task_title = $("#detail_task_form [name='task']").val();
    job = $("#detail_task_form [name='job']").val();

    startdate = $("#detail_task_form [name='startdate']").val();
    enddate = $("#detail_task_form [name='enddate']").val();
    notes = $("#detail_task_form [name='notes']").val();
    completed = $("#detail_task_form [name='completed']").val();

    await axios.patch(`/api/v1/users/${user_id}/tasks/${taskId}`, {
      task_title,
      job_id: job,
      created_at: startdate,
      due_date: enddate,
      completed,
    });
    $("#detailTaskModal").modal("hide");
    location.reload();
  });
});

// Delete button click event handler
$(".delete-button").on("click", async function (e) {
  $(this).closest("li").remove();
  const taskItem = e.target.closest(".list-group-item");
  const taskId = taskItem.dataset.taskId;
  await axios.delete(`/api/v1/users/${user_id}/tasks/${taskId}`);
});
