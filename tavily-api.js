import { tavily } from "@tavily/core";

const tvly = tavily({ apiKey: "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" });
const response = await tvly.search("Who is Leo Messi?");

console.log(response);