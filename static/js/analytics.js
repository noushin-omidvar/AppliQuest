document.addEventListener("DOMContentLoaded", async function () {
  const userId = localStorage.getItem("user_id");

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
});
