// const ctx = $("#myChart");

// new Chart(ctx, {
//   type: "bar",
//   data: {
//     labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
//     datasets: [
//       {
//         label: "# of Votes",
//         data: [12, 19, 3, 5, 2, 3],
//         borderWidth: 1,
//       },
//     ],
//   },
//   options: {
//     scales: {
//       y: {
//         beginAtZero: true,
//       },
//     },
//   },
// });

document.addEventListener("DOMContentLoaded", async function () {
  const userId = localStorage.getItem("user_id");
  console.log(`api/v1/users/${userId}/jobs`);

  resp = await axios.get(`api/v1/users/${userId}/jobs`);
  data = resp.data.jobs;
  const statuses = ["Wishlist", "Applied", "Interview", "Offer", "Rejected"];

  const statusCounts = {};

  for (let i = 0; i < data.length; i++) {
    const status = data[i].status;
    if (status in statusCounts) {
      statusCounts[status]++;
    } else {
      statusCounts[status] = 1;
    }
  }

  const sortedStatusCounts = statuses.map((status) => statusCounts[status]);

  console.log("Job status counts:");
  for (const [status, count] of Object.entries(statusCounts)) {
    console.log(`${status}: ${count}`);
  }

  const funnelChart = document.getElementById("funnelChart").getContext("2d");
  new Chart(funnelChart, {
    type: "funnel",
    data: {
      labels: statuses,
      shrinkAnchor: "top",
      datasets: [
        {
          data: sortedStatusCounts,
          backgroundColor: [
            "#FFCE56",
            "#36A2EB",
            "#f37236",
            "#4BC0C0",
            "#FF6384",
          ],
          hoverBackgroundColor: [
            "#FFCE56",
            "#36A2EB",
            "#f37236",
            "#4BC0C0",
            "#FF6384",
          ],
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        datalabels: {
          color: "#ffffff",
          font: {
            weight: "thin",
          },
          formatter: function (value, context) {
            var label = context.chart.data.labels[context.dataIndex];
            return label + ": " + value.toString();
          },
        },
      },
    },
    plugins: [ChartDataLabels],
  });

  // Create a chart for jobs created over time
  // Filter data for the past year
  const oneYearAgo = new Date();
  oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);

  const filteredData = data.filter((dataPoint) => {
    const date = new Date(dataPoint.created_at);
    console.log(date);
    return date >= oneYearAgo;
  });

  console.log(filteredData);
  // Extract dates and job counts from filtered data
  const utcDates = filteredData.map((dataPoint) => dataPoint.created_at);

  console.log(utcDates);
  // Function to convert UTC date strings to JavaScript Date objects
  function parseUTCDate(dateString) {
    return new Date(dateString);
  }

  // Convert the list of UTC date strings to an array of JavaScript Date objects
  const dates = utcDates.map(parseUTCDate);

  // Count the occurrences of each date
  const dateCounts = {};
  dates.forEach((date) => {
    const dateStr = new Date(date).toLocaleDateString("en-US");
    dateCounts[dateStr] = (dateCounts[dateStr] || 0) + 1;
  });

  // Sort the date keys in ascending order
  const sortedDates = Object.keys(dateCounts).sort(
    (a, b) => new Date(a) - new Date(b)
  );

  // Create an object to store the count of jobs for each day
  const jobCounts = {};

  // Loop through the sortedDates list and count the jobs for each day
  sortedDates.forEach((date) => {
    const formattedDate = moment(date).format("YYYY-MM-DD");
    jobCounts[formattedDate] = (jobCounts[formattedDate] || 0) + 1;
  });

  // Get a reference to the chart container and the chart canvas
  const chartContainer = document.getElementById("chartContainer");
  const ctx = document.getElementById("jobTimeChart").getContext("2d");

  // Create the chart with initial data and options
  const jobChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: sortedDates,
      datasets: [
        {
          label: "Date",
          data: jobCounts,
          backgroundColor: "rgba(0, 123, 255, 0.5)",
          borderColor: "rgba(0, 123, 255, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        x: {
          title: {
            display: true,
            text: "Date",
          },
        },
        y: {
          title: {
            display: true,
            text: "Frequency",
          },
        },
      },
      plugins: {
        legend: {
          display: false,
        },
      },
    },
  });

  // Add event listener to the chart container for button clicks
  chartContainer.addEventListener("click", function (event) {
    if (event.target.classList.contains("chart-button")) {
      const interval = event.target.dataset.interval;
      updateChartView(interval);
    }
  });

  // Function to update the chart view based on the selected interval
  function updateChartView(interval) {
    let newData = [];
    let newLabels = [];

    // Determine the appropriate data and labels based on the selected interval
    if (interval === "day") {
      newData = jobCounts;
      newLabels = sortedDates;
    } else if (interval === "week") {
      // Logic to aggregate data by week
      // You can implement the logic to calculate weekly aggregates here
    } else if (interval === "month") {
      // Logic to aggregate data by month
      // You can implement the logic to calculate monthly aggregates here
    }

    // Update the chart data and labels
    jobChart.data.labels = newLabels;
    jobChart.data.datasets[0].data = newData;

    // Update the chart
    jobChart.update();
  }
});
