---
layout: post
title: "Podcast Alarm history to date"
categories: Development
featured-image: "/images/blog/PodcastAlarmThreeScreens.jpg"
featured-image-alt: "Three screens from Podcast Alarm: Discover, Alarm, Podcast"
description: "Podcast alarm development started in December of 2018 as a weekend project, I wanted to create a utility that would boost my productivity and give me motivation at the start of the day."
permalink: /blog/podcast-alarm-history
redirect_from: /blog/2019/11/13/podcast-alarm-history-to-date-1.html
author: "Jonathan Wilson"
authorImage: "/images/blog/me.jpeg"
---



  <p>Podcast Alarm development started in December of 2018 as a weekend project, I wanted to create a utility that would boost my productivity and give me motivation at the start of the day. The plan was to wake up and have the podcast play throughout the house, letting me go through my daily routine while it played.</p>

  <p>When I began development there was no other apps like it, which is a very rare occurrence in the overcrowded app world. There seemed to have been a version on Android that had been removed and there was mention of someone else making one on a few obscure forums but with no updates in the last year. Reddit and Qura both had questions from people that wanted such an app so it encouraged me to start work.</p>

  <p>I have been a full time iOS engineer for about 6 years so I knew the process of development well. My goal for the app were to maintain as lean of a process as possible. Time, money, and third party expertise was very limited. I needed to do it all, so I wanted to take the path of least resistance.</p>

  <p>To achieve this goal I started by listing the key features needed to achieve the two most basic functions of a podcast alarm.</p>

  <ul>
    <li>Download a podcast episode</li>
    <li>Play that episode at a specified time</li>
  </ul>

  <p>Both of which are much easier said that done, especially the second. After I had determined these It was obvious that my app was a hybrid of an alarm and a podcast application. Which is great because I was able to download lots of great apps that performed each of these functions and investigate what made them popular solutions.</p>

  <p>At this stage I now know what I need to do and also how the app should do it. Next step is to make a mock-up, there is a lot of tools out there for this job but I would recommend the fastest and most flexible one of all, it’s also free; pencil and paper. Print out the outline of a iPhone or iPad and then sketch out your ideas, if they suck rub it out or recycle the whole page.</p>

  <p>At this stage I was ready to start programming. There was a few rules I set myself to make life as easy. I wanted to utilise UIkit as much as possible, with as limited individual styling as possible. This would reduce my reliance on design skills of which I have none. Being able to quickly spin up table views and other UI elements really helped me move quickly. Users generally care much more about usability over design, you can always redesign later on.</p>

  <p>To further improve development speed I would design the UI in a way that could easily make use of reusable elements. It’s a common practice to create buttons etc that can be reused, but I found when I combined it with design it was much more powerful tool. In the end the majority of the app was created with table views and a small handful of cells.</p>

  <p>I will continue this in another post, I hope it gives you an understanding of the development process. In the next post I will talk about some bumps in the road and plans for the future.</p>
