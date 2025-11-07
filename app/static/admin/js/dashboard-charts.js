function weeklyViews() {
  const canvasElement = document.querySelector("canvas#weekly-views");
  let ctx = canvasElement.getContext("2d");

  let get = canvasElement.dataset.get;

  fetch(get, { method: "GET" })
    .then((response) => {
      try {
        return response.json();
      } catch (error) {
        throw new Error(error);
      }
    })
    .catch((e) => {
      console.log(e);
    })
    .then((data) => {
      let obj = new Object({ ...data });
      let cols = [];
      let vals = [];

      for (const [key, value] of Object.entries(obj)) {
        cols.push(key);
        vals.push(value);
      }

      if (document.ctx.views) {
        let chart = document.ctx.views;
        chart.data.labels = cols;
        chart.data.datasets[0].data = vals;

        chart.update();
        return;
      }

      document.ctx.views = new Chart(ctx, {
        type: "bar",
        data: {
          labels: [...cols],
          datasets: [
            {
              label: "Views",
              tension: 0.4,
              borderWidth: 0,
              borderRadius: 4,
              borderSkipped: false,
              backgroundColor: "#43A047",
              data: [...vals],
              barThickness: "flex",
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
          },
          interaction: {
            intersect: false,
            mode: "index",
          },
          scales: {
            y: {
              grid: {
                drawBorder: false,
                display: true,
                drawOnChartArea: true,
                drawTicks: false,
                borderDash: [5, 5],
                color: "#e5e5e5",
              },
              ticks: {
                suggestedMin: 0,
                suggestedMax: 500,
                beginAtZero: true,
                padding: 10,
                font: {
                  size: 14,
                  lineHeight: 2,
                },
                color: "#737373",
              },
            },
            x: {
              grid: {
                drawBorder: false,
                display: false,
                drawOnChartArea: false,
                drawTicks: false,
                borderDash: [5, 5],
              },
              ticks: {
                display: true,
                color: "#737373",
                padding: 10,
                font: {
                  size: 14,
                  lineHeight: 2,
                },
              },
            },
          },
        },
      });

      setInterval(weeklyViews, 10000);
    });
}

function monthlyStudentChart() {
  const canvasElement = document.querySelector("canvas#students-monthly-chart");
  let ctx = canvasElement.getContext("2d");

  let get = canvasElement.dataset.get;

  fetch(get, { method: "GET" })
    .then((response) => {
      try {
        return response.json();
      } catch (error) {
        throw new Error(error);
      }
    })
    .catch((e) => {
      console.log(e);
    })
    .then((data) => {
      let obj = new Object({ ...data });
      let cols = [];
      let vals = [];

      for (const [key, value] of Object.entries(obj)) {
        cols.push(key);
        vals.push(value);
      }

      if (document.ctx.students) {
        let chart = document.ctx.students;
        chart.data.labels = cols;
        chart.data.datasets[0].data = vals;

        chart.update();

        return;
      }
      
      document.ctx.students= new Chart(ctx, {
        type: "bar",
        data: {
          labels: [...cols],
          datasets: [
            {
              label: "Students",
              tension: 0.4,
              borderWidth: 0,
              borderRadius: 4,
              borderSkipped: false,
              backgroundColor: "#43A047",
              data: [...vals],
              barThickness: "flex",
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
          },
          interaction: {
            intersect: false,
            mode: "index",
          },
          scales: {
            y: {
              grid: {
                drawBorder: false,
                display: true,
                drawOnChartArea: true,
                drawTicks: false,
                borderDash: [5, 5],
                color: "#e5e5e5",
              },
              ticks: {
                suggestedMin: 0,
                suggestedMax: 500,
                beginAtZero: true,
                padding: 10,
                font: {
                  size: 14,
                  lineHeight: 2,
                },
                color: "#737373",
              },
            },
            x: {
              grid: {
                drawBorder: false,
                display: false,
                drawOnChartArea: false,
                drawTicks: false,
                borderDash: [5, 5],
              },
              ticks: {
                display: true,
                color: "#737373",
                padding: 10,
                font: {
                  size: 14,
                  lineHeight: 2,
                },
              },
            },
          },
        },
      });

      setInterval(monthlyStudentChart, 10000);
    });
}

function monthlyPaymentChart() {
  const canvasElement = document.querySelector("canvas#monthly-payments-chart");
  let ctx = canvasElement.getContext("2d");

  let get = canvasElement.dataset.get;

  fetch(get, { method: "GET" })
    .then((response) => {
      try {
        return response.json();
      } catch (error) {
        throw new Error(error);
      }
    })
    .catch((e) => {
      console.log(e);
    })
    .then((data) => {
      let obj = new Object({ ...data });
      let cols = [];
      let vals = [];

      for (const [key, value] of Object.entries(obj)) {
        cols.push(key);
        vals.push(value);
      }

      if (document.ctx.payments) {
        let chart = document.ctx.payments;
        chart.data.labels = cols;
        chart.data.datasets[0].data = vals;

        chart.update();

        return;
      }

      document.ctx.payments = new Chart(ctx, {
        type: "line",
        data: {
          labels: [...cols],
          datasets: [
            {
              label: "Payments",
              tension: 0,
              borderWidth: 2,
              pointRadius: 3,
              pointBackgroundColor: "#43A047",
              pointBorderColor: "transparent",
              borderColor: "#43A047",
              backgroundColor: "transparent",
              fill: true,
              data: [...vals],
              maxBarThickness: 6,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            tooltip: {
              callbacks: {
                label: function (context) {
                  const value = context.parsed.y;
                  return (
                    window.appData?.CURRENCY_SYMBOL + value.toLocaleString()
                  );
                },
              },
            },
            legend: {
              display: false,
            },
          },
          interaction: {
            intersect: false,
            mode: "index",
          },
          scales: {
            y: {
              grid: {
                drawBorder: false,
                display: true,
                drawOnChartArea: true,
                drawTicks: false,
                borderDash: [5, 5],
                color: "#e5e5e5",
              },
              ticks: {
                callback: function (value) {
                  return (
                    window.appData?.CURRENCY_SYMBOL + value.toLocaleString()
                  );
                },
                suggestedMin: 0,
                suggestedMax: 500,
                beginAtZero: true,
                padding: 10,
                font: {
                  size: 14,
                  lineHeight: 2,
                },
                color: "#737373",
              },
            },
            x: {
              grid: {
                drawBorder: false,
                display: false,
                drawOnChartArea: false,
                drawTicks: false,
                borderDash: [5, 5],
              },
              ticks: {
                display: true,
                color: "#737373",
                padding: 10,
                font: {
                  size: 14,
                  lineHeight: 2,
                },
              },
            },
          },
        },
      });

      setInterval(monthlyStudentChart, 10000);
    });
}
document.addEventListener("DOMContentLoaded", () => {
  document.ctx = {};

  weeklyViews();

  monthlyStudentChart();
  monthlyPaymentChart();
});
