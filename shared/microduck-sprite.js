/* ORCHESTRA · Adaptateur graphique Microduck (4 directions × 3 poses).
 * Ressources locales issues de la planche fournie. Aucune simulation Python ici.
 * orientation N/E/S/O suit les coordonnées de la grille (y croît vers le bas).
 */
(() => {
  'use strict';
  const orientations = Object.freeze({N:'north',E:'east',S:'south',O:'west'});
  const phases = 3;
  const normalized = direction => orientations[direction] ||
    (['north','east','south','west'].includes(direction) ? direction : 'south');
  const frame = (direction, pose=1) => '../assets/microduck-'+normalized(direction)+'-'+
    Math.max(0,Math.min(phases-1,Math.trunc(pose)||0))+'.webp';
  const facing = (before, after, fallback='E') => {
    if (!before || !after) return fallback;
    const dx=(Array.isArray(after)?after[0]:after.x)-(Array.isArray(before)?before[0]:before.x);
    const dy=(Array.isArray(after)?after[1]:after.y)-(Array.isArray(before)?before[1]:before.y);
    if (Math.abs(dx)+Math.abs(dy)!==1) return fallback;
    return dx>0?'E':dx<0?'O':dy>0?'S':'N';
  };
  window.MicroduckSprite=Object.freeze({frame, facing, orientations, phases});
})();
