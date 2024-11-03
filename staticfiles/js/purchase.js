import { SITE, sendFetchGet, sendFetchPostFile, sendFetchPostWithAccess, sendFetchPut } from "./api.js";
import { changeValue, checkTokens, getCookieValue, createPagination, plugActivity, isMobile, checkMobile, deletePagination } from "./functions.js";

!function () { "use strict"; var e = document.querySelector(".sidebar"), t = document.querySelectorAll("#sidebarToggle, #sidebarToggleTop"); if (e) { e.querySelector(".collapse"); var o = [].slice.call(document.querySelectorAll(".sidebar .collapse")).map((function (e) { return new bootstrap.Collapse(e, { toggle: !1 }) })); for (var n of t) n.addEventListener("click", (function (t) { if (document.body.classList.toggle("sidebar-toggled"), e.classList.toggle("toggled"), e.classList.contains("toggled")) for (var n of o) n.hide() })); window.addEventListener("resize", (function () { if (Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) < 768) for (var e of o) e.hide() })) } var i = document.querySelector("body.fixed-nav .sidebar"); i && i.on("mousewheel DOMMouseScroll wheel", (function (e) { if (Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) > 768) { var t = e.originalEvent, o = t.wheelDelta || -t.detail; this.scrollTop += 30 * (o < 0 ? 1 : -1), e.preventDefault() } })); var l = document.querySelector(".scroll-to-top"); l && window.addEventListener("scroll", (function () { var e = window.pageYOffset; l.style.display = e > 100 ? "block" : "none" })) }();
let totalSum = 0, day;

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

    const MAX_LINES = 100;
    day = new Date().toISOString().split('T')[0];

    lines.forEach((elem) => {
        elem.addEventListener("click", () => {
            elem.classList.toggle("checked_client");
        })
    })
    
    name.textContent = getCookieValue("username");
    purchaseDate.max = day;
    purchaseDate.value = day;

    const getPurchases = (isFirst, func) => {
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
                    } else {
                        func && func();
                    }
                }
            }
        )
    }

    purchaseDate.addEventListener("change", () => {
        day = purchaseDate.value;
        getPurchases();
    });

    sendFetchGet(
        `transactions/transaction_types?offset=0&limit=100`,
        getCookieValue("access"),
        (data) => {
            if (data.errors.length > 0) {
                alert(data.errors[0])
            } else {
                const purchaseID = data.data.items.find((elem) => elem.type === "Закуп").id;
                createLogicForAddModal(purchaseID, getPurchases)
                getPurchases(true);
            }
        }
    )
});


const createLogicForAddModal = (id, fetch) => {
    const addOperationModal = document.querySelector("#add-operation-modal");
    const addOperationModalInputs = addOperationModal.querySelectorAll(".modal-input-text");
    const addOperationModalBtns = addOperationModal.querySelectorAll("button");
    const addOperationOpenModal = document.querySelector(".add-operation");
    const purchaseDate = document.querySelector("#purchase-date");

    const modalActivity = (state) => {
        [...addOperationModalInputs, ...addOperationModalBtns].forEach((elem, i) => {
            elem.style.opacity = state ? 1 : 0.5;
            elem.style.pointerEvents = state ? "auto" : "none";
            elem.tabIndex = state ? i+1 : -1;
        })
    }

    const closeModal = () => {
        const backdrop = document.querySelector(".modal-backdrop");

        addOperationModalInputs.forEach((elem) => elem.value = "");
        addOperationModalInputs[0].style.outline = "none";
        addOperationModalInputs[1].style.outline = "none";
        addOperationModal.classList.remove("show");
        addOperationModal.style.display = "none";
        backdrop.classList.remove("show");
        backdrop.style.zIndex = -1;
    }


    addOperationOpenModal.addEventListener("click", () => {
        const backdrop = document.querySelector(".modal-backdrop");

        backdrop.style.zIndex = 2;
        backdrop.classList.add("show");
        addOperationModal.classList.add("show");
        addOperationModal.style.display = "block";
        addOperationModalInputs[0].focus();
    })

    addOperationModalBtns.forEach((elem, i) => {
        elem.addEventListener("click", () => {
            if (i === 2) {
                if (
                    addOperationModalInputs[0].value.replace(/\+\-/g, "").length > 0 && 
                    addOperationModalInputs[1].value.replace(/\+\-/g, "").length > 0
                ) {
                    modalActivity(false);
                    addOperationModalInputs[0].style.outline = "none";
                    addOperationModalInputs[1].style.outline = "none";

                    sendFetchPostWithAccess(
                        `transactions/`,
                        getCookieValue("access"),
                        {
                            "transaction_type_id": id,
                            "amount": -Number(addOperationModalInputs[0].value),
                            "provider": addOperationModalInputs[1].value,
                        },
                        (data) => {
                            if (data.errors.length > 0) {
                                alert(data.errors[0])
                            } else {
                                day = new Date().toISOString().split('T')[0];
                                purchaseDate.value = day;

                                fetch(
                                    false,
                                    () => {
                                        closeModal();
                                        modalActivity(true);
                                    }
                                )
                            }
                        }
                    )
                } else {
                    if(addOperationModalInputs[0].value.replace(/\+\-/g, "").length <= 0) addOperationModalInputs[0].style.outline = "1px solid red";
                    if(addOperationModalInputs[1].value.replace(/\+\-/g, "").length <= 0) addOperationModalInputs[1].style.outline = "1px solid red";
                }
            } else {
                closeModal();
            }
        })
    })

    document.addEventListener("keypress", () => {
        if (event.key === "Enter" && addOperationModal.classList.contains("show")) { 
            if (
                addOperationModalInputs[0].value.replace(/\+\-/g, "").length > 0 && 
                addOperationModalInputs[1].value.replace(/\+\-/g, "").length > 0
            ) {
                modalActivity(false);
                addOperationModalInputs[0].style.outline = "none";

                sendFetchPostWithAccess(
                    `transactions/`,
                    getCookieValue("access"),
                    {
                        "transaction_type_id": id,
                        "amount": -Number(addOperationModalInputs[0].value),
                        "provider": addOperationModalInputs[1].value,
                    },
                    (data) => {
                        if (data.errors.length > 0) {
                            alert(data.errors[0])
                        } else {
                            day = new Date().toISOString().split('T')[0];
                            purchaseDate.value = day;

                            fetch(
                                false,
                                () => {
                                    closeModal();
                                    modalActivity(true);
                                }
                            )
                        }
                    }
                )
            } else {
                if(addOperationModalInputs[0].value.replace(/\+\-/g, "").length <= 0) addOperationModalInputs[0].style.outline = "1px solid red";
                if(addOperationModalInputs[1].value.replace(/\+\-/g, "").length <= 0) addOperationModalInputs[1].style.outline = "1px solid red";
            }
        }
    })
}
