
document.addEventListener("DOMContentLoaded", function () {
    fetch('/api/productos')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector("table tbody");
            tbody.innerHTML = ""; // Limpia el contenido previo
            data.forEach(producto => {
                const row = `
                    <tr>
                        <td><input type="checkbox" class="selectProduct"></td>
                        <td>${producto.id}</td>
                        <td>${producto.nombre}</td>
                        <td>${producto.descripcion || "Sin descripción"}</td>
                        <td>${producto.categoria}</td>
                        <td>${producto.cantidad}</td>
                        <td>$${producto.precio.toFixed(2)}</td>
                        <td class="text-center">
                            <button class="btn btn-warning btn-sm">✏ Editar</button>
                            <button class="btn btn-danger btn-sm">🗑 Eliminar</button>
                        </td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        })
        .catch(error => console.error("Error al cargar productos:", error));
});
