async function api(
    url,
    options = {}
) {

    const response =
        await fetch(
            url,
            {
                credentials: "same-origin",
                ...options
            }
        );


    const data =
        await response
            .json()
            .catch(
                () => ({})
            );


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Request failed"
        );
    }


    return data;
}


function message(
    text,
    error = false
) {

    const element =
        document.getElementById(
            "form-message"
        );


    if (!element) {
        return;
    }


    element.textContent =
        text;


    element.className =
        "message " +
        (
            error
            ? "error"
            : "success"
        );
}


function setupAuthForm(
    id,
    url
) {

    const form =
        document.getElementById(
            id
        );


    if (!form) {
        return;
    }


    form.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const body =
                Object.fromEntries(
                    new FormData(
                        form
                    ).entries()
                );


            try {

                await api(
                    url,
                    {
                        method:
                            "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                body
                            )
                    }
                );


                location.href =
                    "/dashboard";


            } catch (error) {

                message(
                    error.message,
                    true
                );
            }
        }
    );
}


function setupRegisterForm() {

    const form =
        document.getElementById(
            "register-form"
        );


    if (!form) {
        return;
    }


    form.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const formData =
                new FormData(
                    form
                );


            const password =
                formData.get(
                    "password"
                );


            const confirmPassword =
                formData.get(
                    "confirm_password"
                );


            if (
                password !==
                confirmPassword
            ) {

                message(
                    "Passwords do not match.",
                    true
                );

                return;
            }


            try {

                await api(
                    "/api/register",
                    {
                        method:
                            "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({

                                email:
                                    formData.get(
                                        "email"
                                    ),

                                password:
                                    password
                            })
                    }
                );


                location.href =
                    "/login";


            } catch (error) {

                message(
                    error.message,
                    true
                );
            }
        }
    );
}


function addHomeItem() {

    const container =
        document.getElementById(
            "home-items"
        );


    const row =
        document.createElement(
            "div"
        );


    row.className =
        "item-row";


    row.innerHTML = `

        <input
            name="item_name"
            placeholder="Dining table"
            required
        >

        <input
            name="quantity"
            type="number"
            min="1"
            value="1"
            required
        >

    `;


    container.appendChild(
        row
    );
}


function setupHomePlanner() {

    const form =
        document.getElementById(
            "home-form"
        );


    if (!form) {
        return;
    }


    form.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const formData =
                new FormData(
                    form
                );


            const names =
                [
                    ...form.querySelectorAll(
                        '[name="item_name"]'
                    )
                ];


            const quantities =
                [
                    ...form.querySelectorAll(
                        '[name="quantity"]'
                    )
                ];


            const body = {

                budget:
                    Number(
                        formData.get(
                            "budget"
                        )
                    ),

                room_type:
                    formData.get(
                        "room_type"
                    ),

                style:
                    formData.get(
                        "style"
                    ),

                city:
                    formData.get(
                        "city"
                    ),

                items:
                    names.map(
                        (
                            input,
                            index
                        ) => ({

                            name:
                                input.value,

                            quantity:
                                Number(
                                    quantities[
                                        index
                                    ].value
                                )
                        })
                    )
            };


            try {

                const result =
                    await api(
                        "/api/generate-home",
                        {
                            method:
                                "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    body
                                )
                        }
                    );


                location.href =
                    "/recommendations/" +
                    result.recommendation_id;


            } catch (error) {

                message(
                    error.message,
                    true
                );
            }
        }
    );
}


function setupPartyPlanner() {

    const form =
        document.getElementById(
            "party-form"
        );


    if (!form) {
        return;
    }


    form.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const formData =
                new FormData(
                    form
                );


            const body = {

                budget:
                    Number(
                        formData.get(
                            "budget"
                        )
                    ),

                guests:
                    Number(
                        formData.get(
                            "guests"
                        )
                    ),

                event_type:
                    formData.get(
                        "event_type"
                    ),

                venue:
                    formData.get(
                        "venue"
                    ),

                city:
                    formData.get(
                        "city"
                    ),

                preferences:
                    formData.get(
                        "preferences"
                    )
            };


            try {

                const result =
                    await api(
                        "/api/generate-party",
                        {
                            method:
                                "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    body
                                )
                        }
                    );


                location.href =
                    "/recommendations/" +
                    result.recommendation_id;


            } catch (error) {

                message(
                    error.message,
                    true
                );
            }
        }
    );
}


function setupJewelryPlanner() {

    const form =
        document.getElementById(
            "jewelry-form"
        );


    if (!form) {
        return;
    }


    form.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const formData =
                new FormData(
                    form
                );


            formData.set(
                "budget",
                Number(
                    formData.get(
                        "budget"
                    )
                )
            );


            try {

                const result =
                    await api(
                        "/api/generate-jewelry",
                        {
                            method:
                                "POST",

                            body:
                                formData
                        }
                    );


                location.href =
                    "/recommendations/" +
                    result.recommendation_id;


            } catch (error) {

                message(
                    error.message,
                    true
                );
            }
        }
    );
}


function money(
    value
) {

    return "₹" +
        Number(
            value || 0
        ).toLocaleString(
            "en-IN",
            {
                maximumFractionDigits:
                    0
            }
        );
}


function escapeHtml(
    value
) {

    return String(
        value ?? ""
    ).replace(
        /[&<>"']/g,

        function(character) {

            return {

                "&":
                    "&amp;",

                "<":
                    "&lt;",

                ">":
                    "&gt;",

                '"':
                    "&quot;",

                "'":
                    "&#039;"

            }[character];
        }
    );
}


function escapeAttr(
    value
) {

    return escapeHtml(
        value
    );
}


function renderResult(
    data
) {

    const result =
        data.result ||
        data;


    const sourceNote =
        document.getElementById(
            "source-note"
        );


    if (sourceNote) {

        sourceNote.textContent =
            (
                result.source ===
                "gemini"

                ? "Generated with Gemini"

                : "Generated with local fallback engine"
            )
            +
            " · "
            +
            (
                data.created_at ||
                ""
            );
    }


    const root =
        document.getElementById(
            "recommendation-root"
        );


    if (!root) {
        return;
    }


    const allocation =
        Object.entries(
            result.allocation ||
            {}
        )
        .map(
            (
                [key, value]
            ) => `

                <div class="mini">

                    <span>
                        ${escapeHtml(
                            key.replaceAll(
                                "_",
                                " "
                            )
                        )}
                    </span>

                    <strong>
                        ${money(value)}
                    </strong>

                </div>
            `
        )
        .join("");


    const products =
        (
            result.recommendations ||
            []
        )
        .map(
            item => `

                <div class="product">

                    <div>

                        <span class="tag">

                            ${escapeHtml(
                                item.platform ||
                                "Platform"
                            )}

                        </span>

                        <h3>

                            ${escapeHtml(
                                item.name ||
                                "Recommendation"
                            )}

                        </h3>

                        <p>

                            ${escapeHtml(
                                item.reason ||
                                ""
                            )}

                        </p>

                        <p>

                            ${item.quantity || 1}
                            ×
                            ${money(
                                item.estimated_price
                            )}

                            · subtotal

                            ${money(
                                item.subtotal
                            )}

                        </p>

                    </div>


                    <a
                        class="button secondary"
                        target="_blank"
                        rel="noopener"
                        href="${escapeAttr(
                            item.link || "#"
                        )}"
                    >

                        Search platform

                    </a>

                </div>
            `
        )
        .join("");


    root.innerHTML = `

        <section
            class="card recommendation-card"
        >

            <h2>

                ${escapeHtml(
                    result.summary ||
                    "Your plan"
                )}

            </h2>


            <div class="allocation">

                ${allocation}

            </div>


            ${
                products ||
                `
                    <div class="empty">
                        No recommendations
                        were returned.
                    </div>
                `
            }

        </section>

    `;
}


async function loadRecommendation(
    id
) {

    try {

        const data =
            await api(
                "/api/recommendations-details/" +
                id
            );


        renderResult(
            data
        );


    } catch (error) {

        const root =
            document.getElementById(
                "recommendation-root"
            );


        if (root) {

            root.innerHTML = `

                <div class="card">

                    <p class="message error">

                        ${escapeHtml(
                            error.message
                        )}

                    </p>

                </div>

            `;
        }
    }
}


async function loadHistory(
    target
) {

    const root =
        document.getElementById(
            target
        );


    if (!root) {
        return;
    }


    try {

        const rows =
            await api(
                "/api/history"
            );


        if (!rows.length) {

            root.innerHTML = `

                <div class="card empty">

                    No saved recommendations yet.

                </div>

            `;

            return;
        }


        root.innerHTML =
            rows.map(
                row => `

                    <div
                        class="card history-item"
                    >

                        <div
                            class="row between"
                        >

                            <div>

                                <span class="tag">

                                    ${escapeHtml(
                                        row.planner_type
                                    )}

                                </span>


                                <h3>

                                    ${escapeHtml(
                                        row.result.summary ||
                                        "Recommendation"
                                    )}

                                </h3>


                                <p class="muted">

                                    ${escapeHtml(
                                        row.created_at
                                    )}

                                </p>

                            </div>


                            <a
                                class="button secondary"
                                href="/recommendations/${row.id}"
                            >
                                View
                            </a>

                        </div>

                    </div>

                `
            ).join("");


    } catch (error) {

        root.innerHTML = `

            <div class="card">

                <p class="message error">

                    ${escapeHtml(
                        error.message
                    )}

                </p>

            </div>

        `;
    }
}


async function loadRecentHistory(
    target
) {

    const root =
        document.getElementById(
            target
        );


    if (!root) {
        return;
    }


    try {

        const rows =
            await api(
                "/api/history"
            );


        root.innerHTML =
            rows
                .slice(0, 5)
                .map(
                    row => `

                        <div
                            class="history-item"
                        >

                            <div
                                class="row between"
                            >

                                <span>

                                    <b>
                                        ${escapeHtml(
                                            row.planner_type
                                        )}
                                    </b>

                                    ·

                                    ${escapeHtml(
                                        row.created_at
                                    )}

                                </span>


                                <a
                                    href="/recommendations/${row.id}"
                                >
                                    View
                                </a>

                            </div>

                        </div>

                    `
                )
                .join("")

            ||

            `
                <span class="muted">
                    No plans yet.
                </span>
            `;


    } catch (error) {

        root.innerHTML = `

            <span class="muted">

                Could not load history.

            </span>

        `;
    }
}