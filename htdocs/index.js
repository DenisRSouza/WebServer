fetch('/news.json').then(res => res.json()).then(res => {
    res.forEach(element => {
        const {titulo, subtitulo, conteudo, image_dir, new_dir} = element

        const sect = document.querySelector('.news-home')

        const art = document.createElement('article')

        const h3 = document.createElement('h3')
        h3.textContent = titulo

        const para = document.createElement('p')
        para.textContent = subtitulo

        const img = document.createElement('img')
        img.src = image_dir

        const link = document.createElement('a')
        link.href = new_dir

        link.append(h3, para, img)

        sect.appendChild(link)
    });
})