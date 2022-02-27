export function createUUID() {
  var s = [];
  var hexDigits = "0123456789abcdef";
  for (var i = 0; i < 36; i++) {
    s[i] = hexDigits.substr(Math.floor(Math.random() * 0x10), 1);
  }
  s[14] = "4"; // bits 12-15 of the time_hi_and_version field to 0010
  s[19] = hexDigits.substr((s[19] & 0x3) | 0x8, 1); // bits 6-7 of the clock_seq_hi_and_reserved to 01
  s[8] = s[13] = s[18] = s[23] = "-";

  var uuid = s.join("");
  return uuid;
}

export function deepClone(obj) {
  return JSON.parse(JSON.stringify({ ...obj }));
}

export function isObject(a) {
  return !!a && a.constructor === Object;
}

export function isEmptyObjectCheck(obj) {
  return Object.keys(obj).length === 0 && obj.constructor === Object;
}

export function parseJwt(token) {
  var base64Url = token.split(".")[1];
  var base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
  var jsonPayload = decodeURIComponent(
    atob(base64)
      .split("")
      .map(function(c) {
        return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
      })
      .join("")
  );

  return JSON.parse(jsonPayload);
}

export function getFilterQueryString(filter) {
  let filterKeys = Object.keys(filter);
  let result = filterKeys.reduce((acc, item) => {
    if (filter[item].length || filter[item]) {
      let filteredIds = filter[item].toString();
      acc += `${item}=[${filteredIds}]&`;
    }
    return acc;
  }, "");
  return result.substring(0, result.length - 1);
}

export function getFilterQueryStringWithoutArray(filter) {
  let filterKeys = Object.keys(filter);
  let result = filterKeys.reduce((acc, item) => {
    if (filter[item].length || filter[item]) {
      let filteredIds = filter[item]?.toString();
      acc += `${item}=${filteredIds}&`;
    }
    return acc;
  }, "");
  return result.substring(0, result.length - 1);
}

export function decodePathUrlDataToObject(queryData) {
  let result = {};
  for (const [key, value] of Object.entries(queryData)) {
    let valArray;
    //Add to if condition if the field is single select
    if (key == "page") {
      valArray = parseInt(value.replace(/]|\[/g, ""));
    } else if (
      ["searchTerm", "project_id", "audit_type", "start", "end"].includes(key)
    ) {
      valArray = value.replace(/]|\[/g, "");
    } else {
      valArray = JSON.parse(value);
    }
    result[key] = valArray;
  }
  return result;
}

export const Roles = Object.freeze({
  customer: "customer",
  lead: "lead",
  developer: "developer"
});
