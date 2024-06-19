import { sendFetchGet, sendFetchPut } from "./api.js";
import { checkMobile, checkTokens, getCookieValue, isMobile, parseCurrency, plugActivity } from "./functions.js";

!function () { "use strict"; var e = document.querySelector(".sidebar"), t = document.querySelectorAll("#sidebarToggle, #sidebarToggleTop"); if (e) { e.querySelector(".collapse"); var o = [].slice.call(document.querySelectorAll(".sidebar .collapse")).map((function (e) { return new bootstrap.Collapse(e, { toggle: !1 }) })); for (var n of t) n.addEventListener("click", (function (t) { if (document.body.classList.toggle("sidebar-toggled"), e.classList.toggle("toggled"), e.classList.contains("toggled")) for (var n of o) n.hide() })); window.addEventListener("resize", (function () { if (Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) < 768) for (var e of o) e.hide() })) } var i = document.querySelector("body.fixed-nav .sidebar"); i && i.on("mousewheel DOMMouseScroll wheel", (function (e) { if (Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) > 768) { var t = e.originalEvent, o = t.wheelDelta || -t.detail; this.scrollTop += 30 * (o < 0 ? 1 : -1), e.preventDefault() } })); var l = document.querySelector(".scroll-to-top"); l && window.addEventListener("scroll", (function () { var e = window.pageYOffset; l.style.display = e > 100 ? "block" : "none" })) }();

const change = (value) => { return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".") + " рублей" }

checkTokens().then(() => {
    const name = document.querySelector("#username");
    name.textContent = getCookieValue("username");
    
    const capitalizationSum = document.querySelector("#sum-capitalization");
    const productSum = document.querySelector("#sum-product");
    const cashSum = document.querySelector("#sum-cash");
    const defectiveSum = document.querySelector("#sum-defective");
    const clientsDebtsSum = document.querySelector("#sum-debts");
    const clientsDebtsLink = document.querySelector("#link-debts");
    const productsDebts = document.querySelector("#product-debts");
    const productsDebtsSum = document.querySelector("#sum-product-debts");

    const transactionTypes = ["Наличная сумма"];
    let capSum = 0;

    sendFetchGet(
        `transactions/transaction_types?offset=0&limit=100`,
        getCookieValue("access"),
        (data) => {
            if (data.errors.length > 0) {
                alert(data.errors[0])
            } else {
                let typesArr = [];
                let transactionLink = "transactions/total?";

                transactionTypes.forEach((type) => {
                    data.data.items.forEach((typeObj) => {
                        if(type === typeObj.type){
                            typesArr.push(typeObj.id)
                        }
                    })
                });

                sendFetchGet(
                    transactionLink,
                    getCookieValue("access"),
                    (data) => {
                        if (data.errors.length > 0) {
                            alert(data.errors[0])
                        } else {
                            cashSum.textContent = change(data.data.total);
                            capSum += data.data.total;

                            sendFetchGet(
                                "transactions/debts",
                                getCookieValue("access"),
                                (data) => {
                                    if (data.errors.length > 0) {
                                        alert(data.errors[0])
                                    } else {
                                        clientsDebtsSum.textContent = change(data.data.total);
                                        capSum += Math.abs(data.data.total);

                                        sendFetchGet(
                                            "finances/",
                                            getCookieValue("access"),
                                            (data) => {
                                                if (data.errors.length > 0) {
                                                    alert(data.errors[0])
                                                } else {
                                                    productSum.textContent = change(data.data.amount_in_goods);
                                                    defectiveSum.textContent = change(data.data.amount_in_defects);
                                                    productsDebtsSum.textContent = change(0);
                                                    
                                                    capSum += data.data.amount_in_goods;
                                                    capSum += data.data.amount_in_defects;

                                                    capitalizationSum.textContent = change(capSum);

                                                    plugActivity(false);
                                                    isMobile && checkMobile();
                                                }
                                            }
                                        )
                                    }
                                }
                            )
                        }
                    }
                )
            }
        }
    )
    
    clientsDebtsLink.addEventListener("click", () => {
        window.location = `${window.location.origin}/clients#is_debtor`;
    })

    createLogicForChangeModal();
});


const createLogicForChangeModal = () => {
    const changeModal = document.querySelector("#modal-editor");
    const changeModalInput = changeModal.querySelector(".modal-input-text");
    const changeModalBtns = changeModal.querySelectorAll("button");
    const changeModalTitle = changeModal.querySelector(".modal-title");
    const defectiveCard = document.querySelector("#defective");
    const productCard = document.querySelector("#product");
    const productsDebts = document.querySelector("#product-debts");
    const capitalizationSum = document.querySelector("#sum-capitalization");

    const modalActivity = (state) => {
        [changeModalInput, ...changeModalBtns].forEach((elem) => {
            elem.style.opacity = state ? 1 : 0.5;
            elem.style.pointerEvents = state ? "auto" : "none";
            elem.tabIndex = -1;
        })
    }

    const closeModal = () => {
        const backdrop = document.querySelector(".modal-backdrop");

        changeModalInput.value = "";
        changeModalInput.style.outline = "none";
        changeModal.classList.remove("show");
        changeModal.style.display = "none";
        backdrop.classList.remove("show");
        backdrop.style.zIndex = -1;
    }


    [defectiveCard, productCard, productsDebts].forEach((elem) => {
        elem.addEventListener("click", () => {
            const backdrop = document.querySelector(".modal-backdrop");
            const title = elem.querySelector("#card-name");
            const cardValue = elem.querySelector(".card-value");

            changeModalTitle.textContent = `Изменить статью ${title.textContent}`
            changeModalInput.value = parseCurrency(cardValue.textContent);

            backdrop.style.zIndex = 2;
            backdrop.classList.add("show");
            changeModal.classList.add("show");
            changeModal.style.display = "block";
        })
    })

    changeModalBtns.forEach((elem, i) => {
        elem.addEventListener("click", () => {
            if (i === 2) {
                if (changeModalInput.value.replace(/\+\-/g, "").length > 0) {
                    const productSum = document.querySelector("#sum-product");
                    const defectiveSum = document.querySelector("#sum-defective");

                    modalActivity(false);
                    changeModalInput.style.outline = "none";

                    let objResponse = {};
                    objResponse[
                        changeModalTitle.textContent.includes("товаре") ? 
                            "amount_in_goods" 
                            : 
                            changeModalTitle.textContent.includes("товар") ? "" : "amount_in_defects"
                        ] = Number(changeModalInput.value);

                    sendFetchPut(
                        "finances/update",
                        getCookieValue("access"),
                        objResponse,
                        (data) => {
                            if (data.errors.length > 0) {
                                alert(data.errors[0])
                            } else {
                                const cashSum = document.querySelector("#sum-cash");
                                const clientsDebtsSum = document.querySelector("#sum-debts");
                                const productsDebtsSum = document.querySelector("#sum-product-debts");

                                productSum.textContent = change(data.data.amount_in_goods);
                                defectiveSum.textContent = change(data.data.amount_in_defects);
                                productsDebtsSum.textContent = change(0);

                                capitalizationSum.textContent = change(
                                    data.data.amount_in_goods +
                                    data.data.amount_in_defects +
                                    // data.data.amount_in_defects +
                                    parseCurrency(cashSum.textContent) +
                                    Math.abs(parseCurrency(clientsDebtsSum.textContent))
                                );

                                modalActivity(true);
                                closeModal();
                            }
                        }
                    )
                    
                } else {
                    changeModalInput.style.outline = "1px solid red";
                }
            } else {
                closeModal();
            }
        })
    })
}