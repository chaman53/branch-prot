// utilities/styleHelpers.js
export const getDataTypeClass = (data) => {
  return isNaN(data) ? "text-green" : "text-red";
};
