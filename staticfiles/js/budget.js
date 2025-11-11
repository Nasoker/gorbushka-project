import { sendFetchGet } from "./api.js";
import { changeValue, checkMobile, checkTokens, createPagination, deletePagination, getCookieValue, isMobile, parseJwt, plugActivity } from "./functions.js";

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

checkTokens().then(async () => {
    let day;

    if (!sessionStorage.getItem("transaction_type")) {
        history.back();
    }

    const name = document.querySelector("#username");
    const balance = document.querySelector("#balance");
    const balanceTitle = document.querySelector("#template-title");
    const lines = document.querySelectorAll("tbody > tr")
    const records = document.querySelector("#records");
    const noRecords = document.querySelector("#no-records");
    const reportDate = document.querySelector("#report-date");
    const filter = document.querySelector("#filter");
    const MAX_LINES = 10;
    const ids = JSON.parse(sessionStorage.getItem("transaction_id"));
    const filterNames = JSON.parse(sessionStorage.getItem("transaction_names"));
    const minDate = "2024-06";

    day = new Date().toISOString().slice(0, 7);

    reportDate.min = minDate;
    reportDate.max = day;
    reportDate.value = day;
    
    filterNames.forEach((elem, i) => {
        const select = document.createElement("option");
        select.textContent = elem;
        select.id = ids[i]
        filter.appendChild(select);
    });

    const parsedToken = parseJwt(getCookieValue("access"));

    await sendFetchGet(
        `users/${parsedToken.user_id}`,
        getCookieValue("access"),
        (data) => {
            if (data.errors.length > 0) {
                alert(data.errors[0])
            } else {
                const role = data.data.role;

                if(role === "Customer"){
                    window.location = `${window.location.origin}/orders`;
                } else if(role !== "Admin" && role !== "Depositor"){
                    window.location = `${window.location.origin}/clients`;
                }

                name.textContent = data.data.username;
            }
        }
    )

    let responseTotalLink, responseTransactionLink;
    let currentFilterIds = ids;

    const buildLinks = (selectedDay, filterIds) => {
        if (selectedDay) {
            responseTotalLink = 
                `transactions/total?month=${selectedDay.split('-')[1]}&year=${selectedDay.split('-')[0]}&`;
            responseTransactionLink = 
                `transactions/?month=${selectedDay.split('-')[1]}&year=${selectedDay.split('-')[0]}&offset=0&limit=${MAX_LINES}&`
        } else {
            responseTotalLink = 
                `transactions/total?is_current_month=true&`;
            responseTransactionLink = 
                `transactions/?is_current_month=true&offset=0&limit=${MAX_LINES}&`
        }

        Array.from(filterIds).forEach((elem) => {
            responseTotalLink += `types=${elem}&`;
            responseTransactionLink += `types=${elem}&`;
        });
    }

    buildLinks(day, currentFilterIds);

    const getFilteredTransactions = (isFirst) => {
        sendFetchGet(
            responseTotalLink,
            getCookieValue("access"),
            (data) => {
                if (data.errors.length > 0) {
                    alert(data.errors[0])
                } else {
                    changeValue(balance, data.data.total, true);
                    if(isFirst){
                        balanceTitle.textContent = sessionStorage.getItem("transaction_type");
                    }

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
                                    records.classList.add("active");
                                    noRecords.classList.remove("active");

                                    for (let i = 0; i < MAX_LINES; i++) {
                                        if (i > data.data.items.length - 1) {
                                            lines[i].style.display = "none";
                                        } else {
                                            lines[i].style.display = "table-row";
                                            changeLine(lines[i], data.data.items[i]);
                                        }
                                    }

                                    !isFirst && deletePagination();
                                    createPagination(data, lines, changeLine, "transactions_types");
                                }

                                if(isFirst){
                                    plugActivity(false);
                                    isMobile && checkMobile();
                                    sessionStorage.removeItem("transaction_type");
                                }
                            }
                        }
                    )
                }
            }
        )
    }
    
    getFilteredTransactions(true);

    reportDate.addEventListener("change", () => {
        const selectedDate = reportDate.value;
        const currentDate = new Date().toISOString().slice(0, 7);
        
        if (selectedDate.length === 0 || selectedDate < minDate || selectedDate > currentDate) {
            reportDate.value = currentDate;
            day = currentDate;
        } else {
            day = selectedDate;
        }
        
        buildLinks(day, currentFilterIds);
        getFilteredTransactions(false);
    });

    filter.addEventListener("change", (e) => {
        const changedId = filter.options[ filter.selectedIndex ].id;

        if(changedId === "all") {
            sessionStorage.setItem("transaction_id", JSON.stringify(ids));
            currentFilterIds = ids;
        } else {
            sessionStorage.setItem("transaction_id", JSON.stringify([changedId]));
            currentFilterIds = [changedId];
        }

        buildLinks(day, currentFilterIds);
        getFilteredTransactions(false);
    })
});