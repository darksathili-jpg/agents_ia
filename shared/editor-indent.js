/* ORCHESTRA NSI — indentation Python : logique pure testable et utilisable hors réseau. */
(function(root, factory) {
  const api = factory();
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.OrchestraIndent = api;
})(typeof globalThis === 'object' ? globalThis : this, function() {
  'use strict';
  const STEP = '    ';
  const LINE_BREAK = /\r?\n/;

  function lineStart(text, position) { return text.lastIndexOf('\n', position - 1) + 1; }
  function leadingSpace(text) { return (text.match(/^[ \t]*/) || [''])[0].replace(/\t/g, STEP); }
  function update(value, start, end, insert, caretStart, caretEnd = caretStart) {
    return {value: value.slice(0, start) + insert + value.slice(end), start: caretStart, end: caretEnd};
  }
  function selectedLineRegion(value, start, end) {
    const first = lineStart(value, start);
    // Une sélection finissant exactement au début d'une ligne n'inclut pas cette dernière.
    const lastPos = end > start && value[end - 1] === '\n' ? end - 1 : end;
    const after = value.indexOf('\n', lastPos);
    return {first, after: after < 0 ? value.length : after};
  }
  function indent(value, start, end) {
    if (start === end) return update(value, start, end, STEP, start + 4);
    const {first, after} = selectedLineRegion(value, start, end);
    const old = value.slice(first, after);
    const fresh = old.split('\n').map(line => STEP + line).join('\n');
    const n = old.split('\n').length;
    const adjustedStart = start + 4;
    const adjustedEnd = end + 4 * n;
    return update(value, first, after, fresh, adjustedStart, adjustedEnd);
  }
  function unindent(value, start, end) {
    const {first, after} = selectedLineRegion(value, start, end);
    const old = value.slice(first, after);
    const rows = old.split('\n');
    let removedBeforeStart = 0, removedBeforeEnd = 0, offset = first;
    const lines = rows.map((line, i) => {
      const m = line.match(/^( {1,4}|\t)/);
      const remove = m ? m[0].length : 0;
      if (offset <= start) removedBeforeStart += Math.min(remove, Math.max(0, start - offset));
      if (offset < end || (start === end && offset <= end)) removedBeforeEnd += Math.min(remove, Math.max(0, end - offset));
      offset += line.length + (i < rows.length - 1 ? 1 : 0);
      return line.slice(remove);
    });
    const replacement = lines.join('\n');
    const newStart = Math.max(first, start - removedBeforeStart);
    const newEnd = Math.max(newStart, end - removedBeforeEnd);
    return update(value, first, after, replacement, newStart, newEnd);
  }
  function enter(value, start, end) {
    const line = value.slice(lineStart(value, start), start);
    const whitespace = leadingSpace(line);
    // L'indentation supplémentaire n'est automatique qu'après un « : » final.
    // Les commentaires ne déclenchent pas de bloc (mais une chaîne contenant #
    // est un cas avancé ; les élèves peuvent toujours corriger manuellement).
    const trimmed = line.trim();
    const startsBlock = /^(?:async\s+)?(?:if|elif|else|for|while|def|class|try|except|finally|with|match|case)\b/.test(trimmed) && /:\s*$/.test(trimmed);
    const next = '\n' + whitespace + (startsBlock ? STEP : '');
    return update(value, start, end, next, start + next.length);
  }
  function backspace(value, start, end) {
    if (start !== end || start === 0) return null;
    const before = value.slice(lineStart(value, start), start);
    if (!before || !/^[ ]+$/.test(before)) return null;
    const rem = before.length % 4 || 4;
    return update(value, start - rem, start, '', start - rem);
  }
  function applyToTextarea(textarea, action) {
    let result = null;
    const value = textarea.value;
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    if (action === 'indent') result = indent(value, start, end);
    if (action === 'unindent') result = unindent(value, start, end);
    if (action === 'enter') result = enter(value, start, end);
    if (action === 'backspace') result = backspace(value, start, end);
    if (!result) return false;
    // setRangeText conserve la pile d'annulation native autant que possible.
    let from = 0;
    while(from < value.length && from < result.value.length && value[from] === result.value[from]) from++;
    let oldEnd = value.length, newEnd = result.value.length;
    while(oldEnd > from && newEnd > from && value[oldEnd - 1] === result.value[newEnd - 1]) {oldEnd--; newEnd--;}
    textarea.setRangeText(result.value.slice(from, newEnd), from, oldEnd, 'preserve');
    textarea.setSelectionRange(result.start, result.end);
    textarea.dispatchEvent(new Event('input', {bubbles:true}));
    return true;
  }
  return {indent, unindent, enter, backspace, applyToTextarea};
});
