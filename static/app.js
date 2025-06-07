const search_results = document.querySelector("#search_results")
const input_search = document.querySelector("#input_search")
let my_timer = null

// setTimeout - runs only 1 time
// setInterval - runs forever in intervals
function search(){
    clearInterval(my_timer)
    if (input_search.value != ""){
        my_timer = setTimeout( async function(){
            try{                
                const search_for = input_search.value
                const conn = await fetch(`/search?q=${search_for}`)
                const data = await conn.json()
                search_results.innerHTML = ""
                console.log(data)
                data.forEach(item => {
                    const a = `<div>
                    
                                <a href="/items/${item.item_pk}">
                                <img src="/static/uploads/${item.item_image}" alt="${item.item_name}">
                                </a>

                                <a href="/items/${item.item_pk}">
                                ${item.item_name}
                                </a>

                                </div>`
                    search_results.insertAdjacentHTML("beforeend", a)
                })
                search_results.classList.remove("hidden")
            }catch(err){
                console.error(err)
            }
        }, 500 )
    }else{
        search_results.innerHTML = ""
        search_results.classList.add("hidden")
    }
}



addEventListener("click", function(event){
    if( ! search_results.contains(event.target) ){
        search_results.classList.add("hidden")
    }
    if( input_search.contains(event.target) ){
        search_results.classList.remove("hidden")
    }
})

function add_markers_to_map(data){
    console.log(data)
    data = JSON.parse(data)
    console.log(data)
    data.forEach(item=>{
        // Create custom icon for each marker
        var customIcon = L.divIcon({
            className: 'custom-marker', // Class for custom styling
            html: `<div mix-get="/items/${item.item_pk}" class="custom-marker">${item.item_name.slice(0, 2)}</div>`, // Custom content inside the div
            iconSize: [50, 50], // Size of the div
            iconAnchor: [25, 25], // Anchor point (center of the div)
        });
        
        // Use the custom icon when creating the marker
        L.marker([item.item_lat, item.item_lon], { icon: customIcon }).addTo(map)    
        .openPopup()
    })

    // Make sure mixhtml functionality works on dynamically added elements
    mix_convert()
}


function onMarkerClick(event) {
    alert("Marker clicked at " + event.latlng);
}


document.addEventListener("DOMContentLoaded", function() {
    const deleteProfileBtn = document.getElementById("delete-profile-btn");
    const cancelDeleteBtn = document.getElementById("cancel-delete-btn");
    const deleteConfirmModal = document.getElementById("delete-confirm-modal");
    
    if (deleteProfileBtn) {
        deleteProfileBtn.addEventListener("click", function() {
            deleteConfirmModal.classList.remove("hidden");
        });
    }
    
    if (cancelDeleteBtn) {
        cancelDeleteBtn.addEventListener("click", function() {
            deleteConfirmModal.classList.add("hidden");
        });
    }
});