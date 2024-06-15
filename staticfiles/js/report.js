import { sendFetchGet } from "./api.js";
import { checkMobile, checkTokens, getCookieValue, isMobile, plugActivity } from "./functions.js";

!function () { "use strict"; var e = document.querySelector(".sidebar"), t = document.querySelectorAll("#sidebarToggle, #sidebarToggleTop"); if (e) { e.querySelector(".collapse"); var o = [].slice.call(document.querySelectorAll(".sidebar .collapse")).map((function (e) { return new bootstrap.Collapse(e, { toggle: !1 }) })); for (var n of t) n.addEventListener("click", (function (t) { if (document.body.classList.toggle("sidebar-toggled"), e.classList.toggle("toggled"), e.classList.contains("toggled")) for (var n of o) n.hide() })); window.addEventListener("resize", (function () { if (Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) < 768) for (var e of o) e.hide() })) } var i = document.querySelector("body.fixed-nav .sidebar"); i && i.on("mousewheel DOMMouseScroll wheel", (function (e) { if (Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) > 768) { var t = e.originalEvent, o = t.wheelDelta || -t.detail; this.scrollTop += 30 * (o < 0 ? 1 : -1), e.preventDefault() } })); var l = document.querySelector(".scroll-to-top"); l && window.addEventListener("scroll", (function () { var e = window.pageYOffset; l.style.display = e > 100 ? "block" : "none" })) }();

checkTokens().then(() => {
    const change = (value) => { return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".") + " рублей" }

    const name = document.querySelector("#username");
    const costs = document.querySelector("#costs");
    const costsLink = document.querySelector("#costs-link")
    const netProfit = document.querySelector("#net-profit");
    const profit= document.querySelector("#profit");
    const profitLink = document.querySelector("#profit-link")
    let costsSum, profitSum;
    
    name.textContent = getCookieValue("username");

    sendFetchGet(
        `transactions/total?is_income=false`,
        getCookieValue("access"),
        (data) => {
            if (data.errors.length > 0) {
                alert(data.errors[0])
            } else {
                costsSum = data.data.total;
                costs.textContent = change(costsSum);

                sendFetchGet(
                    `transactions/total?is_income=true`,
                    getCookieValue("access"),
                    (data) => {
                        if (data.errors.length > 0) {
                            alert(data.errors[0])
                        } else {
                            profitSum = data.data.total;
                            profit.textContent = change(profitSum);
                            netProfit.textContent = change(profitSum + costsSum);
                            
                            plugActivity(false);
                            isMobile && checkMobile();
                        }
                    }
                )
            }
        }
    )
    
    
    costsLink.addEventListener("click", () => {
        sessionStorage.setItem("transaction_type", "Расходы");
        window.location = `${window.location.origin}/budget`;
    });

    profitLink.addEventListener("click", () => {
        sessionStorage.setItem("transaction_type", "Доходы");
        window.location = `${window.location.origin}/budget`;
    });
});