async function obtenerDatos() {
    const respuesta = await fetch('https://tu-backend.com/datos'); // Reemplaza con tu endpoint
    const datos = await respuesta.json();
    return datos;
}

const contenedor = document.getElementById('contenedor-datos');

obtenerDatos().then(datos => {
    contenedor.innerHTML = `
        <p>Nombre: ${datos.nombre}</p>
        <p>Edad: ${datos.edad}</p>
        <p>Ciudad: ${datos.ciudad}</p>
    `;
});