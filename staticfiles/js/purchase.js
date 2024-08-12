import { SITE, sendFetchGet, sendFetchPostFile, sendFetchPostWithAccess, sendFetchPut } from "./api.js";
import { changeValue, checkTokens, getCookieValue, createPagination, plugActivity, isMobile, checkMobile, deletePagination } from "./functions.js";

!function () { "use strict"; var e = document.querySelector(".sidebar"), t = document.querySelectorAll("#sidebarToggle, #sidebarToggleTop"); if (e) { e.querySelector(".collapse"); var o = [].slice.call(document.querySelectorAll(".sidebar .collapse")).map((function (e) { return new bootstrap.Collapse(e, { toggle: !1 }) })); for (var n of t) n.addEventListener("click", (function (t) { if (document.body.classList.toggle("sidebar-toggled"), e.classList.toggle("toggled"), e.classList.contains("toggled")) for (var n of o) n.hide() })); window.addEventListener("resize", (function () { if (Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) < 768) for (var e of o) e.hide() })) } var i = document.querySelector("body.fixed-nav .sidebar"); i && i.on("mousewheel DOMMouseScroll wheel", (function (e) { if (Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) > 768) { var t = e.originalEvent, o = t.wheelDelta || -t.detail; this.scrollTop += 30 * (o < 0 ? 1 : -1), e.preventDefault() } })); var l = document.querySelector(".scroll-to-top"); l && window.addEventListener("scroll", (function () { var e = window.pageYOffset; l.style.display = e > 100 ? "block" : "none" })) }();
let totalSum = 0;

const changeLine = (node, value) => {
    const children = Array.from(node.children);
    const keys = ["provider", "total"];

    children.forEach((elem, i) => {
        if (i === keys.length - 1) {
            elem.classList.remove("text-success");
            elem.classList.remove("text-danger");
            changeValue(elem, value[keys[i]])
        } else {
            elem.textContent = value[keys[i]];
        }
    })
}

checkTokens().then(() => {
    const lines = document.querySelectorAll("tbody > tr");
    const name = document.querySelector("#username");
    const records = document.querySelector("#records");
    const noRecords = document.querySelector("#no-records");
    const purchaseDate = document.querySelector("#purchase-date");
    const totalPurchases = document.querySelector("#total-purchase");

    const MAX_LINES = 30;
    let day = new Date().toISOString().split('T')[0];

    lines.forEach((elem) => {
        elem.addEventListener("click", () => {
            elem.classList.toggle("checked_client");
        })
    })
    
    name.textContent = getCookieValue("username");
    purchaseDate.max = day;
    purchaseDate.value = day;

    const getPurchases = (isFirst) => {
        totalSum = 0;

        sendFetchGet(
            `transactions/provider_total?offset=0&limit=${MAX_LINES}&on_date=${day}`,
            getCookieValue("access"),
            (data) => {
                if (data.errors.length > 0) {
                    alert(data.errors[0])
                } else {
                    const transactions = data.data.items;

                    if (data.data.pagination.total === 0) {
                        records.classList.remove("active");
                        noRecords.classList.add("active");                        
                    } else {
                        records.classList.add("active");
                        noRecords.classList.remove("active");

                        for (let i = 0; i < MAX_LINES; i++) {
                            if (i > transactions.length - 1) {
                                lines[i].style.display = "none";
                            } else {
                                totalSum += transactions[i].total;
                                lines[i].style.display = "table-row";
                                lines[i].classList.remove("checked_client");    
                                changeLine(lines[i], transactions[i]);
                            }
                        }
                        
                        changeValue(totalPurchases, totalSum, true);
                    }

                    if(isFirst){
                        plugActivity(false);
                        isMobile && checkMobile();
                    }
                }
            }
        )
    }

    purchaseDate.addEventListener("change", () => {
        day = purchaseDate.value;
        getPurchases();
    });

    getPurchases(true);
});
