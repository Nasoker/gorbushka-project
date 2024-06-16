import { sendFetchGet } from "./api.js";
import { checkMobile, checkTokens, getCookieValue, isMobile, plugActivity } from "./functions.js";

!function () { "use strict"; var e = document.querySelector(".sidebar"), t = document.querySelectorAll("#sidebarToggle, #sidebarToggleTop"); if (e) { e.querySelector(".collapse"); var o = [].slice.call(document.querySelectorAll(".sidebar .collapse")).map((function (e) { return new bootstrap.Collapse(e, { toggle: !1 }) })); for (var n of t) n.addEventListener("click", (function (t) { if (document.body.classList.toggle("sidebar-toggled"), e.classList.toggle("toggled"), e.classList.contains("toggled")) for (var n of o) n.hide() })); window.addEventListener("resize", (function () { if (Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) < 768) for (var e of o) e.hide() })) } var i = document.querySelector("body.fixed-nav .sidebar"); i && i.on("mousewheel DOMMouseScroll wheel", (function (e) { if (Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) > 768) { var t = e.originalEvent, o = t.wheelDelta || -t.detail; this.scrollTop += 30 * (o < 0 ? 1 : -1), e.preventDefault() } })); var l = document.querySelector(".scroll-to-top"); l && window.addEventListener("scroll", (function () { var e = window.pageYOffset; l.style.display = e > 100 ? "block" : "none" })) }();

function parseCurrency(str) {
    // Удаляем все точки и слова из строки
    let cleanedStr = str.replace(/[^\d]/g, '');
    // Преобразуем полученную строку в число
    return parseInt(cleanedStr, 10);
}

checkTokens().then(() => {
    const change = (value) => { return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".") + " рублей" }

    const name = document.querySelector("#username");
    const capitalizationSum = document.querySelector("#sum-capitalization");
    const productSum = document.querySelector("#sum-product");
    const cashSum = document.querySelector("#sum-cash");
    const defectiveSum = document.querySelector("#sum-defective");
    const clientsDebtsSum = document.querySelector("#sum-debts");
    const clientsDebtsLink = document.querySelector("#link-debts");
    const transactionTypes = ["Сумма в товаре", "Наличная сумма", "Сумма в браке"]
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
                name.textContent = getCookieValue("username");

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
                                        productSum.textContent = change(0);
                                        defectiveSum.textContent = change(0);
                                        capSum += Math.abs(data.data.total);
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


    [defectiveCard, productCard].forEach((elem) => {
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
                    // modalActivity(false);
                    // changeModalInputs[0].style.outline = "none";
                    
                    
                } else {
                    changeModalInput.style.outline = "1px solid red";
                }
            } else {
                closeModal();
            }
        })
    })
}