//'use strict';

const elangames = document.querySelector('#elangamesplayed');

fetch('http://localhost:5000/getGamesPlayed/terice1')
  .then((response) => response.json())
  .then((data) => console.log(data));

const names = ['Elan', 'John', 'Michael', 'Will', 'Brij'];
const combined_names = ['ElanJohn', 'ElanMichael', 'JohnMichael'];
const names_to_summoner_name = {
  Elan: 'terice1',
  John: 'Mrs%20Fizzle',
  Michael: 'kickboy9',
  Will: 'QuadForm',
  Brij: 'yeehaw342',
};

names.forEach((name) => {
  summoner_name = names_to_summoner_name[name];

  updateGamesPlayed(name, summoner_name);
  updateWinrate(name, summoner_name);
  updateDamagerate(name, summoner_name);
  updateWinrateMostDamage(name, summoner_name);
  updateMultiKills(name, summoner_name);
  updateDamage(name, summoner_name);
  updateKills(name, summoner_name);
  updateDeaths(name, summoner_name);
});

combined_names.forEach((combined_name) => {
  split_names = combined_name.split(/(?=[A-Z])/);
  name1 = split_names[0];
  name2 = split_names[1];
  summoner1 = names_to_summoner_name[name1];
  summoner2 = names_to_summoner_name[name2];

  updateCombinedWinrate(name1, name2, summoner1, summoner2);
  updateCombinedMostDamageRate(name1, name2, summoner1, summoner2);
  updateCombinedWinrateDamage(name1, name2, summoner1, summoner2);
});

function updateGamesPlayed(name, summoner_name) {
  const selector = document.querySelector('#' + name + 'gamesplayed');

  url = 'http://localhost:5000/getGamesPlayed/' + summoner_name;
  fetch(url)
    .then((response) => response.json())
    .then((games) => (selector.textContent = `${games} games played`));
}

function updateWinrate(name, summoner_name) {
  const wins_selector = document.querySelector('#' + name + 'wins');
  const losses_selector = document.querySelector('#' + name + 'losses');
  const winrate_selector = document.querySelector('#' + name + 'winrate');

  url = 'http://localhost:5000/getWinrate/' + summoner_name;
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      wins_selector.textContent = data.num_wins + ' wins';
      losses_selector.textContent = data.num_games - data.num_wins + ' losses';
      winrate_selector.textContent = data.winrate + ' winrate';
    });
}

function updateDamagerate(name, summoner_name) {
  const damage_selector = document.querySelector('#' + name + 'timesmostdamage');
  const damagerate_selector = document.querySelector('#' + name + 'mostdamagerate');

  url = 'http://localhost:5000/getDamageRate/' + summoner_name;
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      damage_selector.textContent = `Dealt most damage ${data.times_most_damage} times `;
      damagerate_selector.textContent = `${data.damage_rate} most damage rate`;
    });
}

function updateWinrateMostDamage(name, summoner_name) {
  const winrate_most_damage_selector = document.querySelector('#' + name + 'winratemostdamage');

  url = 'http://localhost:5000/getWinrateWhenMostDamage/' + summoner_name;
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      winrate_most_damage_selector.textContent = `${data.winrate} winrate when dealt most damage`;
    });
}

function updateMultiKills(name, summoner_name) {
  const pentakills_selector = document.querySelector('#' + name + 'pentakills');
  const quadrakills_selector = document.querySelector('#' + name + 'quadrakills');

  url = 'http://localhost:5000/getMultikills/' + summoner_name;
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      pentakills_selector.textContent = `${data.pentakills} pentakills`;
      quadrakills_selector.textContent = `${data.quadrakills} quadrakills`;
    });
}

function updateDamage(name, summoner_name) {
  const average_damage_selector = document.querySelector('#' + name + 'avgdamage');
  const max_damage_selector = document.querySelector('#' + name + 'maxdamage');

  url = 'http://localhost:5000/getDamageStats/' + summoner_name;
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      average_damage_selector.textContent = `Average damage of ${data.average_damage}`;
      max_damage_selector.textContent = `Max damage of ${data.max_damage}`;
    });
}

function updateKills(name, summoner_name) {
  const average_kills_selector = document.querySelector('#' + name + 'avgkills');
  const max_kills_selector = document.querySelector('#' + name + 'maxkills');

  url = 'http://localhost:5000/getKillStats/' + summoner_name;
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      average_kills_selector.textContent = `Average kills of ${data.average_kills}`;
      max_kills_selector.textContent = `Max kills of ${data.max_kills}`;
    });
}

function updateDeaths(name, summoner_name) {
  const average_deaths_selector = document.querySelector('#' + name + 'avgdeaths');
  const max_deaths_selector = document.querySelector('#' + name + 'maxdeaths');

  url = 'http://localhost:5000/getDeathStats/' + summoner_name;
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      average_deaths_selector.textContent = `Average deaths of ${data.average_deaths}`;
      max_deaths_selector.textContent = `Max deaths of ${data.max_deaths}`;
    });
}

function updateCombinedWinrate(name1, name2, summoner1, summoner2) {
  const games_selector = document.querySelector('#' + name1 + name2 + 'games');
  const winrate_selector = document.querySelector('#' + name1 + name2 + 'winrate');

  url = 'http://localhost:5000/getWinrateForPlayers/' + summoner1 + '/' + summoner2;
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      winrate_selector.textContent = `${name1} and ${name2} played ${data.games} games together and have a ${data.winrate} 
      winrate`;
      games_selector.textContent = `They won ${data.wins} games and lost ${data.games - data.wins} games`;
    });
}

function updateCombinedMostDamageRate(name1, name2, summoner1, summoner2) {
  const name1_damage_selector = document.querySelector('#' + name1 + name2 + name1 + 'mostdamage');
  const name2_damage_selector = document.querySelector('#' + name1 + name2 + name2 + 'mostdamage');

  url = 'http://localhost:5000/getDamageRateTwoPlayers/' + summoner1 + '/' + summoner2;
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      name1_damage_selector.textContent = `${name1} has dealt the most damage ${data.num_times_most_damage} times and has a ${data.damage_rate} most damage rate`;
    });

  url = 'http://localhost:5000/getDamageRateTwoPlayers/' + summoner2 + '/' + summoner1;
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      name2_damage_selector.textContent = `${name2} has dealt the most damage ${data.num_times_most_damage} times and has a ${data.damage_rate} most damage rate`;
    });
}

function updateCombinedWinrateDamage(name1, name2, summoner1, summoner2) {
  const name1_winrate_selector = document.querySelector('#' + name1 + name2 + name1 + 'winratedamage');
  const name2_winrate_selector = document.querySelector('#' + name1 + name2 + name2 + 'winratedamage');

  url = 'http://localhost:5000/getWinrateWhenMostDamageTwoPlayers/' + summoner1 + '/' + summoner2;
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      name1_winrate_selector.textContent = `They won ${data.num_wins} games when ${name1} did the most damage with a ${data.winrate} winrate`;
    });

  url = 'http://localhost:5000/getWinrateWhenMostDamageTwoPlayers/' + summoner2 + '/' + summoner1;
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      name2_winrate_selector.textContent = `They won ${data.num_wins} games when ${name2} did the most damage with a ${data.winrate} winrate`;
    });
}
