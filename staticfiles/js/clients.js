import { sendFetchGet, sendFetchPostWithAccess } from "./api.js";
import { checkTokens, getCookieValue, createPagination, changeValue, plugActivity, checkMobile, isMobile, deletePagination } from "./functions.js";

!function () { "use strict"; var e = document.querySelector(".sidebar"), t = document.querySelectorAll("#sidebarToggle, #sidebarToggleTop"); if (e) { e.querySelector(".collapse"); var o = [].slice.call(document.querySelectorAll(".sidebar .collapse")).map((function (e) { return new bootstrap.Collapse(e, { toggle: !1 }) })); for (var n of t) n.addEventListener("click", (function (t) { if (document.body.classList.toggle("sidebar-toggled"), e.classList.toggle("toggled"), e.classList.contains("toggled")) for (var n of o) n.hide() })); window.addEventListener("resize", (function () { if (Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) < 768) for (var e of o) e.hide() })) } var i = document.querySelector("body.fixed-nav .sidebar"); i && i.on("mousewheel DOMMouseScroll wheel", (function (e) { if (Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) > 768) { var t = e.originalEvent, o = t.wheelDelta || -t.detail; this.scrollTop += 30 * (o < 0 ? 1 : -1), e.preventDefault() } })); var l = document.querySelector(".scroll-to-top"); l && window.addEventListener("scroll", (function () { var e = window.pageYOffset; l.style.display = e > 100 ? "block" : "none" })) }();

const changeLine = (node, value) => {
    const children = Array.from(node.children);
    const keys = ["name", "telegram", "phone", "balance"];
    node.id = value.id;

    children.forEach((elem, i) => {
        if (keys[i] === "balance") {
            elem.classList.remove("text-success");
            elem.classList.remove("text-danger");
            changeValue(elem, value[keys[i]])
        } else if (keys[i] === "name") {
            elem.textContent = `${value.first_name} ${value.last_name}`;
        } else if (keys[i] === "telegram") {
            elem.textContent = `@${value.telegram}`;
        } else if (keys[i] === "phone") {
            elem.textContent = value.phone;
        }
    })
}

checkTokens().then(() => {
    const lines = document.querySelectorAll("tbody > tr")
    const name = document.querySelector("#username");
    const search = document.querySelector("#search");
    const searchButton = document.querySelector("#search-btn");
    const linkOnlyForAdmins = document.querySelectorAll("#onlyForAdmin");
    const records = document.querySelector("#records");
    const noRecords = document.querySelector("#no-records");

    getCookieValue("role") === "Moderator" && linkOnlyForAdmins.forEach((elem) => elem.remove());
    const MAX_LINES = 10;

    name.textContent = getCookieValue("username");

    const getCustomersByDefinedName = () => {
        const requestLink = window.location.hash === "#is_debtor" ? 
            `users/customers?name=${search.value}&limit=&is_debtor=true` :
            `users/customers?name=${search.value}&limit=${MAX_LINES}`

        sendFetchGet(
            requestLink,
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
                        
                        data.id = search.value;

                        deletePagination();
                        createPagination(data, lines, changeLine, "definedCustomers");
                    }
                }
            }
        )
    }

    lines.forEach((elem) => {
        elem.addEventListener("click", (e) => {
            e.preventDefault();
            sessionStorage.setItem("client_id", elem.id);
            window.location = `${window.location.origin}/client`;
        });
    });


    const requestLink = window.location.hash === "#is_debtor" ? 
            `users/customers?&limit=${MAX_LINES}&is_debtor=true` :
            `users/customers?&limit=${MAX_LINES}`

    sendFetchGet(
        requestLink,
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

                    createPagination(data, lines, changeLine, "customers");
                }

                plugActivity(false);
                isMobile && checkMobile();
            }
        }
    )

    search.addEventListener('keypress', function (e) {
        // если пользователь нажал на Enter
        if (e.which === 13) {
            getCustomersByDefinedName()
        }
    });

    searchButton.addEventListener("click", () => {
        getCustomersByDefinedName();
    })
});