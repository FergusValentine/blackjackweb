function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim()
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

let cards = [
    [127136],
    [127137, 127138, 127139, 127140, 127141, 127142, 127143, 127144, 127145, 127146, 127147, 127149, 127150],
    [127153, 127154, 127155, 127156, 127157, 127158, 127159, 127160, 127161, 127162, 127163, 127165, 127166],
    [127169, 127170, 127171, 127172, 127173, 127174, 127175, 127176, 127177, 127178, 127179, 127181, 127182],
    [127185, 127186, 127187, 127188, 127189, 127190, 127191, 127192, 127193, 127194, 127195, 127197, 127198],
]

const api = "/api/blackjack/"

let game_response = null

async function FetchData(method, context) {
    try{
        const parameters =
        {
            method: method,
            headers: {"Content-Type": "application/json", 'X-CSRFToken': csrftoken},
        }

        if(context){
            parameters.body = JSON.stringify(context);
        }

        const response = await fetch(api, parameters);

        if (!response.ok){
            console.log("Failed to fetch data");
            return;
        }

        const text = await response.text();
        return text ? JSON.parse(text) : undefined;
    }
    catch(err){
        console.log(err);
    }
}

function UpdateHandHTML(hand, id) {
    document.getElementById(id).innerHTML = "";

    function AddCardToHand(card) {
        let rank = card.rank - 1

        if(rank < 0)
            rank = 0;

        let card_icon = cards[card.suit][rank];
        let player_hand = document.getElementById(id)
        player_hand.innerHTML += "&#" + card_icon + ";"
    }

    hand.forEach(AddCardToHand)
}

function GetElement(id) {
    return document.getElementById(id)
}

function DealerTurn() {
    UpdateHandHTML(game_response.dealer.hand, "dealer-cards")

    let dealerHand = game_response.dealer.count
    let playerHand = game_response.player.count
    let text = ""

    if (playerHand > 21){
        text = "You Bust, you lose!"
    }
    else if(dealerHand > 21){
        text = "Dealer bust, you win!"
    }
    else if(playerHand === dealerHand){
        text = "You drew!"
    }
    else if(playerHand < dealerHand){
        text = "You lose!"
    }
    else if(playerHand > dealerHand){
        text = "You win!"
    }

    GetElement("victory-message").innerText = text
    GetElement("victory-screen").style = "block"
    GetElement("restart").style.display = "inline-block";
    GetElement("hit").disabled = true;
    GetElement("stand").disabled = true;
}

async function HitAction() {
    game_response = await FetchData("POST", {action: "hit"});

    UpdateHandHTML(game_response.player.hand, "player-cards")

    if(game_response.over){
        GetElement("hit").disabled = true;
        GetElement("stand").disabled = true;
        DealerTurn();
    }
}

async function StandAction() {
    GetElement("hit").disabled = true;
    GetElement("stand").disabled = true;

    game_response = await FetchData("POST", {action: "stand"});
    DealerTurn();
}

async function LoadPage()
{
    game_response = await FetchData("GET");

    UpdateHandHTML(game_response.player.hand, "player-cards")
    UpdateHandHTML(game_response.dealer.hand, "dealer-cards")

    GetElement("victory-message").innerText = ""
    GetElement("victory-screen").style.display = "none"
    GetElement("restart").style.display = "none"

    GetElement("hit").disabled = true;
    GetElement("stand").disabled = true;

    if(game_response.over){
        DealerTurn();
    }
    else
    {
        GetElement("hit").disabled = false;
        GetElement("stand").disabled = false;
    }
}

async function RestartPage()
{
    let j =await FetchData("POST", {action: "restart"});

    GetElement("victory-message").innerText = ""
    GetElement("victory-screen").style = "none"
    GetElement("restart").style.display = "none"

    GetElement("hit").disabled = true;
    GetElement("stand").disabled = true;

    game_response = await FetchData("GET");

    UpdateHandHTML(game_response.player.hand, "player-cards")
    UpdateHandHTML(game_response.dealer.hand, "dealer-cards")

    GetElement("hit").disabled = false;
    GetElement("stand").disabled = false;
}

document.addEventListener("DOMContentLoaded", () =>
{
    GetElement("restart").onclick = RestartPage;
    GetElement("hit").onclick = HitAction
    GetElement("stand").onclick = StandAction;

    LoadPage()
});