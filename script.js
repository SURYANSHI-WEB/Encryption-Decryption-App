// ── State ───────────────────────────────────────────────────────────────────
const modes = {
  caesar: 'encrypt',
  vigenere: 'encrypt',
  base64: 'encrypt',
  morse: 'encrypt'
};

// ── Cipher Logic ────────────────────────────────────────────────────────────

function runCaesar() {
  const input = document.getElementById('caesar-input').value;
  const shift = parseInt(document.getElementById('caesar-shift').value) || 3;
  let s = modes.caesar === 'decrypt' ? (26 - shift) % 26 : shift;
  document.getElementById('caesar-output').value = input.split('').map(c => {
    if (/[a-z]/.test(c)) return String.fromCharCode(((c.charCodeAt(0) - 97 + s) % 26) + 97);
    if (/[A-Z]/.test(c)) return String.fromCharCode(((c.charCodeAt(0) - 65 + s) % 26) + 65);
    return c;
  }).join('');
}

function runROT13() {
  const input = document.getElementById('rot13-input').value;
  document.getElementById('rot13-output').value = input.split('').map(c => {
    if (/[a-z]/.test(c)) return String.fromCharCode(((c.charCodeAt(0) - 97 + 13) % 26) + 97);
    if (/[A-Z]/.test(c)) return String.fromCharCode(((c.charCodeAt(0) - 65 + 13) % 26) + 65);
    return c;
  }).join('');
}

function runVigenere() {
  const input = document.getElementById('vigenere-input').value;
  const key = document.getElementById('vigenere-key').value.toUpperCase().replace(/[^A-Z]/g, '');
  if (!key) { document.getElementById('vigenere-output').value = input; return; }
  const decrypt = modes.vigenere === 'decrypt';
  let ki = 0;
  document.getElementById('vigenere-output').value = input.split('').map(c => {
    if (/[a-zA-Z]/.test(c)) {
      const base = /[a-z]/.test(c) ? 97 : 65;
      const shift = key.charCodeAt(ki % key.length) - 65;
      ki++;
      const s = decrypt ? (26 - shift) % 26 : shift;
      return String.fromCharCode(((c.charCodeAt(0) - base + s) % 26) + base);
    }
    return c;
  }).join('');
}

function runAtbash() {
  const input = document.getElementById('atbash-input').value;
  document.getElementById('atbash-output').value = input.split('').map(c => {
    if (/[a-z]/.test(c)) return String.fromCharCode(122 - (c.charCodeAt(0) - 97));
    if (/[A-Z]/.test(c)) return String.fromCharCode(90 - (c.charCodeAt(0) - 65));
    return c;
  }).join('');
}

function runBase64() {
  const input = document.getElementById('base64-input').value;
  try {
    document.getElementById('base64-output').value = modes.base64 === 'encrypt'
      ? btoa(unescape(encodeURIComponent(input)))
      : decodeURIComponent(escape(atob(input)));
  } catch {
    document.getElementById('base64-output').value = '⚠ Invalid Base64 input';
  }
}

const MORSE = {
  A:'.-',B:'-...',C:'-.-.',D:'-..',E:'.',F:'..-.',G:'--.',H:'....',I:'..',J:'.---',
  K:'-.-',L:'.-..',M:'--',N:'-.',O:'---',P:'.--.',Q:'--.-',R:'.-.',S:'...',T:'-',
  U:'..-',V:'...-',W:'.--',X:'-..-',Y:'-.--',Z:'--..',
  '0':'-----','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....',
  '6':'-....','7':'--...','8':'---..','9':'----.',
  '.':'.-.-.-',',':'--..--','?':'..--..','!':'-.-.--','/':'-..-.','@':'.--.-.'
};
const MORSE_REV = Object.fromEntries(Object.entries(MORSE).map(([k,v]) => [v,k]));

function runMorse() {
  const input = document.getElementById('morse-input').value;
  if (modes.morse === 'encrypt') {
    document.getElementById('morse-output').value = input.toUpperCase().split('').map(c => {
      if (c === ' ') return '/';
      return MORSE[c] || c;
    }).join(' ');
  } else {
    document.getElementById('morse-output').value = input.trim().split(' / ').map(word =>
      word.split(' ').map(code => MORSE_REV[code] || '?').join('')
    ).join(' ');
  }
}

const runners = { caesar: runCaesar, rot13: runROT13, vigenere: runVigenere, atbash: runAtbash, base64: runBase64, morse: runMorse };

// ── Utilities ────────────────────────────────────────────────────────────────

function clearPanel(name) {
  document.getElementById(name + '-input').value = '';
  document.getElementById(name + '-output').value = '';
}

function copyOutput(cipher) {
  const val = document.getElementById(cipher + '-output').value;
  if (!val) return;
  navigator.clipboard.writeText(val);
  const fb = document.getElementById('copy-' + cipher);
  fb.classList.add('show');
  setTimeout(() => fb.classList.remove('show'), 2000);
}

// ── Event Listeners ──────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {

  // Tab switching
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const cipher = tab.dataset.cipher;
      document.querySelectorAll('.cipher-panel').forEach(p => p.classList.remove('active'));
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.getElementById('panel-' + cipher).classList.add('active');
      tab.classList.add('active');
    });
  });

  // Mode toggle (encrypt/decrypt)
  document.querySelectorAll('.mode-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const cipher = btn.dataset.cipher;
      const mode = btn.dataset.mode;
      modes[cipher] = mode;
      btn.closest('.mode-toggle').querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      if (runners[cipher]) runners[cipher]();
    });
  });

  // Run buttons
  document.querySelectorAll('[data-run]').forEach(btn => {
    btn.addEventListener('click', () => {
      const cipher = btn.dataset.run;
      if (runners[cipher]) runners[cipher]();
    });
  });

  // Clear buttons
  document.querySelectorAll('[data-clear]').forEach(btn => {
    btn.addEventListener('click', () => clearPanel(btn.dataset.clear));
  });

  // Copy buttons
  document.querySelectorAll('[data-copy]').forEach(btn => {
    btn.addEventListener('click', () => copyOutput(btn.dataset.copy));
  });

  // Live input on textareas
  document.querySelectorAll('textarea[id$="-input"]').forEach(ta => {
    const cipher = ta.id.replace('-input', '');
    ta.addEventListener('input', () => { if (runners[cipher]) runners[cipher](); });
  });

  // Caesar shift live update
  document.getElementById('caesar-shift').addEventListener('input', runCaesar);

  // Vigenere key live update
  document.getElementById('vigenere-key').addEventListener('input', runVigenere);

  // Morse reference toggle
  document.getElementById('morse-ref-toggle').addEventListener('click', () => {
    document.getElementById('morse-ref').classList.toggle('show');
  });

  // Build morse reference grid
  const grid = document.getElementById('morse-grid');
  Object.entries(MORSE).forEach(([char, code]) => {
    const el = document.createElement('div');
    el.className = 'morse-item';
    el.innerHTML = `${char} <span>${code}</span>`;
    grid.appendChild(el);
  });

});