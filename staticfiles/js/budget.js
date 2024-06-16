import { sendFetchGet } from "./api.js";
import { changeValue, checkMobile, checkTokens, createPagination, getCookieValue, isMobile, plugActivity } from "./functions.js";

!function () { "use strict"; var e = document.querySelector(".sidebar"), t = document.querySelectorAll("#sidebarToggle, #sidebarToggleTop"); if (e) { e.querySelector(".collapse"); var o = [].slice.call(document.querySelectorAll(".sidebar .collapse")).map((function (e) { return new bootstrap.Collapse(e, { toggle: !1 }) })); for (var n of t) n.addEventListener("click", (function (t) { if (document.body.classList.toggle("sidebar-toggled"), e.classList.toggle("toggled"), e.classList.contains("toggled")) for (var n of o) n.hide() })); window.addEventListener("resize", (function () { if (Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) < 768) for (var e of o) e.hide() })) } var i = document.querySelector("body.fixed-nav .sidebar"); i && i.on("mousewheel DOMMouseScroll wheel", (function (e) { if (Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) > 768) { var t = e.originalEvent, o = t.wheelDelta || -t.detail; this.scrollTop += 30 * (o < 0 ? 1 : -1), e.preventDefault() } })); var l = document.querySelector(".scroll-to-top"); l && window.addEventListener("scroll", (function () { var e = window.pageYOffset; l.style.display = e > 100 ? "block" : "none" })) }();

const changeLine = (node, value) => {
    const children = Array.from(node.children);
    const keys = ["created_at", "amount", "transaction_type", "comment"];

    const formatDate = (dateString) => {
        const date = new Date(dateString);

        const day = date.getDate();
        const month = date.getMonth() + 1; // Месяцы в объекте Date начинаются с 0, поэтому добавляем 1
        const year = date.getFullYear();

        return day + "." + month + "." + year;
    }

    children.forEach((elem, i) => {
        if (typeof (value[keys[i]]) === "number") {
            elem.classList.remove("text-success");
            elem.classList.remove("text-danger");
            changeValue(elem, value[keys[i]])
        } else {
            elem.textContent = i === 0 ? formatDate(value[keys[i]]) : value[keys[i]];
        }
    })
}

checkTokens().then(() => {
    if (!sessionStorage.getItem("transaction_type")) {
        history.back();
    }

    const name = document.querySelector("#username");
    const balance = document.querySelector("#balance");
    const balanceTitle = document.querySelector("#template-title");
    const lines = document.querySelectorAll("tbody > tr")
    const records = document.querySelector("#records");
    const noRecords = document.querySelector("#no-records");
    const MAX_LINES = 10;

    const responseTotalLink = sessionStorage.getItem("transaction_type") === "Ежедневная прибыль" ?
        `transactions/total?types=${sessionStorage.getItem("transaction_id")}&is_current_month=true`
        :
        `transactions/total?is_income=false&is_current_month=true`

    const responseTransactionLink = sessionStorage.getItem("transaction_type") === "Ежедневная прибыль" ?
        `transactions/?types=${sessionStorage.getItem("transaction_id")}&is_current_month=true&offset=0&limit=${MAX_LINES}`
        :
        `transactions/?is_income=false&is_current_month=true&offset=0&limit=${MAX_LINES}`

    name.textContent = getCookieValue("username");
    sendFetchGet(
        responseTotalLink,
        getCookieValue("access"),
        (data) => {
            if (data.errors.length > 0) {
                alert(data.errors[0])
            } else {
                changeValue(balance, data.data.total, true);
                balanceTitle.textContent = sessionStorage.getItem("transaction_type");
                sendFetchGet(
                    responseTransactionLink,
                    getCookieValue("access"),
                    (data) => {
                        if (data.errors.length > 0) {
                            alert(data.errors[0])
                        } else {
                            if (data.data.pagination.total === 0) {
                                records.classList.remove("active");
                                noRecords.classList.add("active");
                            } else {
                                for (let i = 0; i < MAX_LINES; i++) {
                                    if (i > data.data.items.length - 1) {
                                        lines[i].style.display = "none";
                                    } else {
                                        lines[i].style.display = "table-row";
                                        changeLine(lines[i], data.data.items[i]);
                                    }
                                }
                                data.id = sessionStorage.getItem("transaction_type");
                                createPagination(data, lines, changeLine, "transactions_types");
                            }

                            sessionStorage.removeItem("transaction_type");
            
                            plugActivity(false);
                            isMobile && checkMobile();
                        }
                    }
                )
            }
        }
    )
});