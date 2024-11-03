import { sendFetchGet, sendFetchPost } from "./api.js";
import { getCookieValue, parseJwt } from "./functions.js";

const email = document.querySelector("#exampleInputEmail");
const password = document.querySelector("#exampleInputPassword");
const loginBtn = document.querySelector(".btn_login");
const formUser = document.querySelector(".user");

const loginActivity = (state) => {
    [email, password, loginBtn].forEach((elem, i) => {
        elem.style.opacity = state ? 1 : 0.5;
        elem.style.pointerEvents = state ? "auto" : "none";
    })
}

if(getCookieValue("role") && getCookieValue("refresh")){
    loginActivity(false);
    sendFetchPost(
        "token/refresh",
        {
            "refresh": getCookieValue("refresh"),
        },
        (data) => {
            if(data.code === "token_not_valid"){
                document.cookie = `access=; path=/; expires=-1`;
                document.cookie = `refresh=; path=/; expires=-1`;
                document.cookie = `id=; path=/; expires=-1`;
                document.cookie = `username=; path=/; expires=-1`;
                document.cookie = `role=; path=/ expires=-1;`;
                document.cookie = `phone=; path=/; expires=-1`;
                document.cookie = `telegram=; path=/; expires=-1`;
                loginActivity(true);
                return
            } else {
                document.cookie = `access=${data.access}; path=/; max-age=3600`;
                document.cookie = `refresh=${data.refresh}; path=/; max-age=${3600 * 24 * 3}`;
                window.location = getCookieValue("role") === "Customer" ? `${window.location.origin}/orders` : `${window.location.origin}/clients`;
            }
        }
    );
}

formUser.addEventListener("submit", (e) => {
    e.preventDefault();
});

loginBtn.addEventListener("click", () => {
    if (password.value.length > 0 && email.value.length > 0) {
        loginActivity(false);
        sendFetchPost(
            "token/pair",
            {
                "username": email.value,
                "password": password.value,
            },
            (data) => {
                if (data.detail) {
                    loginActivity(true);
                    password.style.outline = "1px solid red";
                    email.style.outline = "1px solid red";
                    alert(data.detail);
                } else {
                    const parsedToken = parseJwt(data.access);
                    document.cookie = `access=${data.access}; path=/; max-age=3600`;
                    document.cookie = `refresh=${data.refresh}; path=/; max-age=${3600 * 24 * 3}`;
                    document.cookie = `id=${parsedToken.user_id}; path=/;`;
                    
                    sendFetchGet(
                        `users/${parsedToken.user_id}`,
                        data.access,
                        (data) => {
                            if(data.errors.length > 0){
                                alert(data.errors[0])
                            }else{
                                document.cookie = `username=${data.data.first_name} ${data.data.last_name}; path=/;`;
                                document.cookie = `role=${data.data.role}; path=/;`;
                                document.cookie = `phone=${data.data.phone}; path=/;`;
                                document.cookie = `telegram=${data.data.telegram}; path=/;`;
    
                                window.location = data.data.role === "Customer" ? `${window.location.origin}/orders` : `${window.location.origin}/clients`;
                            }
                        }
                    )
                }
            }
        )
    } else {
        password.style.outline = password.value.length === 0 ? "1px solid red" : "none";
        email.style.outline = email.value.length === 0 ? "1px solid red" : "none";
    }
});

[email, password].forEach((elem) => {
    elem.addEventListener("input", (e) => {
        elem.style.outline = elem.value.length === 0 ? "1px solid red" : "none";
    });

    elem.addEventListener("click", (e) => {
        elem.style.outline = elem.value.length === 0 ? "1px solid red" : "none";
    })
});