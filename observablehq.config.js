// See https://observablehq.com/framework/config for documentation.
export const header = `
  <div class="header">
    <div class="header-centered">
      <a href="/">Overview</a>
      <a href="/peloton">Peloton</a>
      <a href="/races">Races</a>
      <a href="/insights">Insights</a>
    </div>
  </div>
`;

export default {
  // The app’s title; used in the sidebar and webpage titles.
  title: "Tour de Data",

  // Content to add to the head of the page, e.g. for a favicon:
  head: '<link rel="icon" href="logo.png" type="image/png" sizes="32x32">',

  // The pages and sections in the sidebar. If you don’t specify this option,
  // all pages will be listed in alphabetical order. Listing pages explicitly
  // lets you organize them into sections and have unlisted pages.
  // pages: [
  //   {
  //     name: "Examples",
  //     pages: [
  //       {name: "Dashboard", path: "/example-dashboard"},
  //       {name: "Report", path: "/example-report"}
  //     ]
  //   }
  // ],


  // The path to the source root.
  root: "src",

  // Some additional configuration options and their defaults:
  footer: "", // what to show in the footer (HTML)
  sidebar: false, // whether to show the sidebar
  pager: false, // whether to show previous & next links in the footer
  // theme: "cotton", // try "light", "dark", "slate", etc.
  header: header, // what to show in the header (HTML)
  style: "./custom-style.css", // path to a custom CSS stylesheet
  toc: false, // whether to show the table of contents
  // output: "dist", // path to the output root for build
  // search: true, // activate search
  // linkify: true, // convert URLs in Markdown to links
  // typographer: false, // smart quotes and other typographic improvements
  // preserveExtension: false, // drop .html from URLs
  // preserveIndex: false, // drop /index from URLs
  
  interpreters: {
    ".py": ["python"]
  },

};
