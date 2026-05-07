// ── Mode State ───────────────────────────────────────────────────────────────
// Each cipher remembers if we're encrypting or decrypting
var caesarMode  = 'encrypt';
var vigenereMode = 'encrypt';
var base64Mode  = 'encode';
var morseMode   = 'encrypt';
var stegMode    = 'encrypt';


// ── Tab Switching ─────────────────────────────────────────────────────────────
function switchTab(name) {
  // Hide all panels and deactivate all tabs
  var panels = document.querySelectorAll('.cipher-panel');
  for (var i = 0; i < panels.length; i++) {
    panels[i].classList.remove('active');
  }
  var tabs = document.querySelectorAll('.tab');
  for (var i = 0; i < tabs.length; i++) {
    tabs[i].classList.remove('active');
  }

  // Show the selected panel and mark its tab active
  document.getElementById('panel-' + name).classList.add('active');
  event.target.classList.add('active');
}


// ── Mode Setters ──────────────────────────────────────────────────────────────
function setCaesarMode(mode) {
  caesarMode = mode;
  document.getElementById('caesar-encrypt-btn').classList.toggle('active', mode === 'encrypt');
  document.getElementById('caesar-decrypt-btn').classList.toggle('active', mode === 'decrypt');
  runCaesar();
}

function setVigenereMode(mode) {
  vigenereMode = mode;
  document.getElementById('vigenere-encrypt-btn').classList.toggle('active', mode === 'encrypt');
  document.getElementById('vigenere-decrypt-btn').classList.toggle('active', mode === 'decrypt');
  runVigenere();
}

function setBase64Mode(mode) {
  base64Mode = mode;
  document.getElementById('base64-encrypt-btn').classList.toggle('active', mode === 'encode');
  document.getElementById('base64-decrypt-btn').classList.toggle('active', mode === 'decode');
  runBase64();
}

function setMorseMode(mode) {
  morseMode = mode;
  document.getElementById('morse-encrypt-btn').classList.toggle('active', mode === 'encrypt');
  document.getElementById('morse-decrypt-btn').classList.toggle('active', mode === 'decrypt');
  runMorse();
}

function setStegMode(mode) {
  stegMode = mode;
  document.getElementById('steg-encrypt-btn').classList.toggle('active', mode === 'encrypt');
  document.getElementById('steg-decrypt-btn').classList.toggle('active', mode === 'decrypt');
}


// ── Utility: Clear & Copy ─────────────────────────────────────────────────────
function clearPanel(name) {
  document.getElementById(name + '-input').value = '';
  document.getElementById(name + '-output').value = '';
}

function copyOutput(name) {
  var output = document.getElementById(name + '-output').value;
  if (!output) return;
  navigator.clipboard.writeText(output);
  var feedback = document.getElementById('copy-' + name);
  feedback.classList.add('show');
  setTimeout(function() {
    feedback.classList.remove('show');
  }, 2000);
}


// ── Caesar Cipher ─────────────────────────────────────────────────────────────
function runCaesar() {
  var input = document.getElementById('caesar-input').value;
  var shift = parseInt(document.getElementById('caesar-shift').value) || 3;

  // If decrypting, reverse the shift
  if (caesarMode === 'decrypt') {
    shift = (26 - shift) % 26;
  }

  var result = '';
  for (var i = 0; i < input.length; i++) {
    var c = input[i];
    if (c >= 'a' && c <= 'z') {
      result += String.fromCharCode(((c.charCodeAt(0) - 97 + shift) % 26) + 97);
    } else if (c >= 'A' && c <= 'Z') {
      result += String.fromCharCode(((c.charCodeAt(0) - 65 + shift) % 26) + 65);
    } else {
      result += c; // keep spaces, numbers, punctuation as-is
    }
  }

  document.getElementById('caesar-output').value = result;
}


// ── ROT13 ─────────────────────────────────────────────────────────────────────
// ROT13 is its own inverse so no mode needed
function runROT13() {
  var input = document.getElementById('rot13-input').value;
  var result = '';
  for (var i = 0; i < input.length; i++) {
    var c = input[i];
    if (c >= 'a' && c <= 'z') {
      result += String.fromCharCode(((c.charCodeAt(0) - 97 + 13) % 26) + 97);
    } else if (c >= 'A' && c <= 'Z') {
      result += String.fromCharCode(((c.charCodeAt(0) - 65 + 13) % 26) + 65);
    } else {
      result += c;
    }
  }
  document.getElementById('rot13-output').value = result;
}


// ── Vigenère Cipher ───────────────────────────────────────────────────────────
function runVigenere() {
  var input = document.getElementById('vigenere-input').value;
  var key = document.getElementById('vigenere-key').value.toUpperCase().replace(/[^A-Z]/g, '');

  // If no key just pass through unchanged
  if (!key) {
    document.getElementById('vigenere-output').value = input;
    return;
  }

  var result = '';
  var keyIndex = 0;

  for (var i = 0; i < input.length; i++) {
    var c = input[i];
    if (/[a-zA-Z]/.test(c)) {
      var base = (c >= 'a' && c <= 'z') ? 97 : 65;
      var shift = key.charCodeAt(keyIndex % key.length) - 65;
      if (vigenereMode === 'decrypt') {
        shift = (26 - shift) % 26;
      }
      result += String.fromCharCode(((c.charCodeAt(0) - base + shift) % 26) + base);
      keyIndex++;
    } else {
      result += c;
    }
  }

  document.getElementById('vigenere-output').value = result;
}


// ── Atbash Cipher ─────────────────────────────────────────────────────────────
// Atbash mirrors the alphabet so A=Z, B=Y, etc. Also its own inverse.
function runAtbash() {
  var input = document.getElementById('atbash-input').value;
  var result = '';
  for (var i = 0; i < input.length; i++) {
    var c = input[i];
    if (c >= 'a' && c <= 'z') {
      result += String.fromCharCode(122 - (c.charCodeAt(0) - 97));
    } else if (c >= 'A' && c <= 'Z') {
      result += String.fromCharCode(90 - (c.charCodeAt(0) - 65));
    } else {
      result += c;
    }
  }
  document.getElementById('atbash-output').value = result;
}


// ── Base64 ────────────────────────────────────────────────────────────────────
function runBase64() {
  var input = document.getElementById('base64-input').value;
  var result = '';
  try {
    if (base64Mode === 'encode') {
      result = btoa(unescape(encodeURIComponent(input)));
    } else {
      result = decodeURIComponent(escape(atob(input)));
    }
  } catch (e) {
    result = '⚠ Invalid Base64 input';
  }
  document.getElementById('base64-output').value = result;
}


// ── Morse Code ────────────────────────────────────────────────────────────────
var MORSE_MAP = {
  A:'.-',  B:'-...', C:'-.-.', D:'-..',  E:'.',    F:'..-.',
  G:'--.',  H:'....', I:'..',   J:'.---', K:'-.-',  L:'.-..',
  M:'--',   N:'-.',   O:'---',  P:'.--.',  Q:'--.-', R:'.-.',
  S:'...',  T:'-',    U:'..-',  V:'...-', W:'.--',  X:'-..-',
  Y:'-.--', Z:'--..',
  '0':'-----','1':'.----','2':'..---','3':'...--','4':'....-',
  '5':'.....','6':'-....','7':'--...','8':'---..','9':'----.',
  '.':'.-.-.-', ',':'--..--', '?':'..--..', '!':'-.-.--',
  '/':'-..-.', '@':'.--.-.'
};

// Build a reverse map: morse code → letter
var MORSE_REVERSE = {};
for (var letter in MORSE_MAP) {
  MORSE_REVERSE[MORSE_MAP[letter]] = letter;
}

function runMorse() {
  var input = document.getElementById('morse-input').value;
  var result = '';

  if (morseMode === 'encrypt') {
    // Text → Morse: each letter becomes a code, spaces become /
    var chars = input.toUpperCase().split('');
    var parts = [];
    for (var i = 0; i < chars.length; i++) {
      if (chars[i] === ' ') {
        parts.push('/');
      } else if (MORSE_MAP[chars[i]]) {
        parts.push(MORSE_MAP[chars[i]]);
      } else {
        parts.push(chars[i]); // keep unknown chars
      }
    }
    result = parts.join(' ');
  } else {
    // Morse → Text: split by / for words, split by space for letters
    var words = input.trim().split(' / ');
    var decodedWords = [];
    for (var w = 0; w < words.length; w++) {
      var codes = words[w].split(' ');
      var word = '';
      for (var c = 0; c < codes.length; c++) {
        word += MORSE_REVERSE[codes[c]] || '?';
      }
      decodedWords.push(word);
    }
    result = decodedWords.join(' ');
  }

  document.getElementById('morse-output').value = result;
}

function toggleMorseRef() {
  document.getElementById('morse-ref').classList.toggle('show');
}

// Build the Morse reference chart on page load
function buildMorseChart() {
  var grid = document.getElementById('morse-grid');
  for (var letter in MORSE_MAP) {
    var item = document.createElement('div');
    item.className = 'morse-item';
    item.innerHTML = letter + ' <span>' + MORSE_MAP[letter] + '</span>';
    grid.appendChild(item);
  }
}

buildMorseChart();


// ── Steganography (needs Flask backend running) ───────────────────────────────
async function runSteg() {
  var imageFile = document.getElementById('steg-image').files[0];
  var message   = document.getElementById('steg-input').value;
  var outputBox = document.getElementById('steg-output');
  var status    = document.getElementById('steg-status');

  if (!imageFile) {
    status.innerText = '⚠ Please upload an image first.';
    return;
  }

  var formData = new FormData();
  formData.append('image', imageFile);
  status.innerText = 'Processing…';

  try {
    if (stegMode === 'encrypt') {
      // Hiding a message inside the image
      if (!message) {
        status.innerText = '⚠ Enter a message to hide.';
        return;
      }
      formData.append('message', message);

      var response = await fetch('http://127.0.0.1:5000/api/hide', { method: 'POST', body: formData });
      if (!response.ok) throw new Error('Server returned an error');

      // Download the returned image
      var blob = await response.blob();
      var url  = window.URL.createObjectURL(blob);
      var link = document.createElement('a');
      link.href = url;
      link.download = 'vault_image.png';
      document.body.appendChild(link);
      link.click();
      link.remove();

      outputBox.value = "Your secret is hidden in 'vault_image.png'. Check your downloads folder.";
      status.innerText = '✅ Image downloaded!';

    } else {
      // Revealing a hidden message from the image
      var response = await fetch('http://127.0.0.1:5000/api/reveal', { method: 'POST', body: formData });
      var data = await response.json();

      if (data.message) {
        outputBox.value = data.message;
        status.innerText = '✅ Message revealed!';
      } else {
        outputBox.value = data.error || 'No hidden message found.';
        status.innerText = '❌ Nothing found.';
      }
    }
  } catch (err) {
    console.error(err);
    status.innerText = '❌ Server error. Is Flask running?';
  }
}