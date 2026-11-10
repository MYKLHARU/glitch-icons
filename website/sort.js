'use strict';

function compareGlitchIcons(a, b, order, featuredRank) {
  const name = a.name.localeCompare(b.name, undefined, {numeric:true, sensitivity:'base'});
  if (order === 'newest') {
    return ((Date.parse(b.addedAt) || 0) - (Date.parse(a.addedAt) || 0)) || name;
  }
  if (order === 'az') return name;
  if (order === 'za') return -name;
  return (featuredRank.get(a.file) ?? 9999) - (featuredRank.get(b.file) ?? 9999) || name;
}

if (typeof module !== 'undefined') module.exports = compareGlitchIcons;
