import { sendFetchGet } from "./api.js";
import { checkMobile, checkTokens, getCookieValue, isMobile, plugActivity } from "./functions.js";

!function () { "use strict"; var e = document.querySelector(".sidebar"), t = document.querySelectorAll("#sidebarToggle, #sidebarToggleTop"); if (e) { e.querySelector(".collapse"); var o = [].slice.call(document.querySelectorAll(".sidebar .collapse")).map((function (e) { return new bootstrap.Collapse(e, { toggle: !1 }) })); for (var n of t) n.addEventListener("click", (function (t) { if (document.body.classList.toggle("sidebar-toggled"), e.classList.toggle("toggled"), e.classList.contains("toggled")) for (var n of o) n.hide() })); window.addEventListener("resize", (function () { if (Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) < 768) for (var e of o) e.hide() })) } var i = document.querySelector("body.fixed-nav .sidebar"); i && i.on("mousewheel DOMMouseScroll wheel", (function (e) { if (Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) > 768) { var t = e.originalEvent, o = t.wheelDelta || -t.detail; this.scrollTop += 30 * (o < 0 ? 1 : -1), e.preventDefault() } })); var l = document.querySelector(".scroll-to-top"); l && window.addEventListener("scroll", (function () { var e = window.pageYOffset; l.style.display = e > 100 ? "block" : "none" })) }();

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
    const transactionElems = [productSum, cashSum, defectiveSum];

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
                            capitalizationSum.textContent = change(data.data.total);
                        }
                    }
                )

                typesArr.forEach((elem, i) => {
                    sendFetchGet(
                        transactionLink + `types=${elem}`,
                        getCookieValue("access"),
                        (data) => {
                            if (data.errors.length > 0) {
                                alert(data.errors[0])
                            } else {
                                transactionElems[i].textContent = change(data.data.total);
                                plugActivity(false);
                                isMobile && checkMobile();
                            }
                        }
                    )
                })

                sendFetchGet(
                    "transactions/debts",
                    getCookieValue("access"),
                    (data) => {
                        if (data.errors.length > 0) {
                            alert(data.errors[0])
                        } else {
                            clientsDebtsSum.textContent = change(data.data.total);
                        }
                    }
                )
            }
        }
    )
    
    clientsDebtsLink.addEventListener("click", () => {
        window.location = "./clients.html#is_debtor";
    })
});