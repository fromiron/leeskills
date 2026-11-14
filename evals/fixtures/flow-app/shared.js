// State shared by both variants of the flow-app fixture. Everything stays in
// sessionStorage; nothing is sent anywhere.
const store = {
  sets() { return JSON.parse(sessionStorage.getItem("flowapp.sets") || "[]"); },
  addSet(set) { sessionStorage.setItem("flowapp.sets", JSON.stringify([...this.sets(), set])); },
  clear() { sessionStorage.removeItem("flowapp.sets"); },
  offline() { return sessionStorage.getItem("flowapp.offline") === "1"; },
  setOffline(value) { sessionStorage.setItem("flowapp.offline", value ? "1" : "0"); },
};

if (new URLSearchParams(location.search).get("offline") === "1") store.setOffline(true);

function renderSets(list) {
  list.replaceChildren(...store.sets().map((set) => {
    const item = document.createElement("li");
    item.textContent = `${set.exercise}: ${set.weight} kg × ${set.reps}`;
    return item;
  }));
}

// A labeled test control, not part of the product: it simulates the connection.
function mountFixtureControl() {
  const bar = document.createElement("aside");
  bar.className = "fixture-control";
  bar.setAttribute("aria-label", "Fixture control");
  bar.innerHTML = '<div class="row"><span>Fixture control: connection is <strong id="connection-state"></strong></span><button type="button" id="toggle-connection"></button></div>';
  document.body.append(bar);
  const paint = () => {
    document.getElementById("connection-state").textContent = store.offline() ? "offline" : "online";
    document.getElementById("toggle-connection").textContent = store.offline() ? "Go online" : "Go offline";
  };
  document.getElementById("toggle-connection").addEventListener("click", () => { store.setOffline(!store.offline()); paint(); });
  paint();
}
document.addEventListener("DOMContentLoaded", mountFixtureControl);
