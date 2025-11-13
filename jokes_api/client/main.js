window.addEventListener("DOMContentLoaded", () => {
    const selLang = document.getElementById("selLang");
    const selCat = document.getElementById("selCat");
    const selNum = document.getElementById("selNum");
    const selCustomJoke = document.getElementById("selCustomJoke");
    const btnAmuse = document.getElementById("btnAmuse");
    const jokesContent = document.getElementById("jokesContent");

    const languageMap = {
        any: "ANY",
        cs: "CZECH",
        de: "GERMAN",
        en: "ENGLISH",
        es: "SPANISH",
        eu: "BASQUE",
        fr: "FRENCH",
        gl: "GALICIAN",
        hu: "HUNGARIAN",
        it: "ITALIAN",
        lt: "LITHUANIAN",
        pl: "POLISH",
        sv: "SWEDISH"
    };

    Object.entries(languageMap).forEach(([code, name]) => {
        const opt = document.createElement("option");
        opt.value = code;
        opt.textContent = name;
        selLang.appendChild(opt);
    });

    const allnum = document.createElement("option");
    allnum.value = 0;
    allnum.textContent = "all";
    selNum.appendChild(allnum);

    for (let i = 1; i <= 10; i++) {
        const opt = document.createElement("option");
        opt.value = i;
        opt.textContent = i;
        selNum.appendChild(opt);
    }

    btnAmuse.addEventListener("click", async (e) => {
        e.preventDefault();
        jokesContent.innerHTML = "";

        const jokeId = selCustomJoke.value.trim();
        if (jokeId !== "") {
            if (jokeId >= 0) {
                try {
                    const res = await fetch(`https://cs330-jokes.onrender.com/api/v1/jokes/${jokeId}`);
                    if (!res.ok) {
                        const errorData = await res.json();
                        throw new Error(errorData.error || "Unknown error");
                    }
                    const data = await res.json();
                    jokesContent.innerHTML = `<article class="box has-background-link-light mb-3">${data.joke.text}</article>`;
                } catch (err) {
                    jokesContent.innerHTML = `<article class="box has-background-danger-light mb-3">${err.message}</article>`;
                }
                return;
            } else {
                jokesContent.innerHTML = `<article class="box has-background-danger-light mb-3">Joke ID must be positive and a number!</article>`;
                return;
            }
        }

        const language = selLang.value;
        const category = selCat.value;
        const number = selNum.value;

        const endpoint = category === "all"
            ? `https://cs330-jokes.onrender.com/api/v1/jokes/${language}/any/${number}`
            : `https://cs330-jokes.onrender.com/api/v1/jokes/${language}/${category}/${number}`;

        try {
            const res = await fetch(endpoint);
            if (!res.ok) {
                const errorData = await res.json();
                throw new Error(errorData.error || "Unknown error");
            }
            const data = await res.json();

            if (data.jokes.length === 0) {
                jokesContent.innerHTML = `<article class="box has-background-danger-light mb-3">There is no joke for the combination of language and category</article>`;
            } else {
                data.jokes.forEach(j => {
                    const article = document.createElement("article");
                    article.className = "box has-background-link-light mb-3";
                    article.textContent = j.text;
                    jokesContent.appendChild(article);
                });
            }
        } catch (err) {
            jokesContent.innerHTML = `<article class="box has-background-danger-light mb-3">${err.message}</article>`;
        }
    });
});
