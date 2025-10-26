"use client";

import React, { useEffect, useState } from "react";
import { motion, useReducedMotion } from "framer-motion";

import mainHomeImg from "../assets/homePic.png";
import secondaryHomeImg from "../assets/secondaryHomePic.png";

export default function Home() {
  const prefersReduced = useReducedMotion();
  const [ready, setReady] = useState(false);
  const [shouldAnimate, setShouldAnimate] = useState(false);

  useEffect(() => {
    // run on client only
    const done = sessionStorage.getItem("homeHeroAnimated");
    if (!done) {
      setShouldAnimate(true);
      sessionStorage.setItem("homeHeroAnimated", "1");
    }
    setReady(true); // now we know whether to animate
  }, []);

  const mainAnim = prefersReduced || !shouldAnimate
    ? { initial: false, animate: { opacity: 1, scale: 1 } }
    : { initial: { opacity: 0, scale: 0.98 }, animate: { opacity: 1, scale: 1 }, transition: { duration: 0.6, ease: "easeOut", delay: 0.1 } };

  const insetAnim = prefersReduced || !shouldAnimate
    ? { initial: false, animate: { opacity: 1, y: 0 } }
    : { initial: { opacity: 0, y: 24 }, animate: { opacity: 1, y: 0 }, transition: { duration: 0.55, ease: "easeOut", delay: 0.25 } };

  if (!ready) {
    // first render (SSR or before effect): render static markup to avoid mismatches
    return (
      <section className="bg-[var(--color-bg)] space-12">
        <div className="mx-auto max-w-7xl px-4 py-12 sm:py-16 md:py-20">
          <div className="grid items-center gap-10 md:grid-cols-2 lg:gap-16">
            <div className="order-2 md:order-1">
              <h1 className="text-[80px] leading-none tracking-wide sm:text-[72px] md:text-[92px]">Arcana</h1>
              <div className="mt-4 max-w-lg rounded p-4 text-zinc-800">
                Arcana is an AI-powered interior design platform that transforms any room photo or sketch into photorealistic, purchasable designs in seconds. Powered by Anthropic’s Claude multi-agent system and ControlNet, Arcana intelligently understands your style, optimizes layouts, and curates real furniture within your budget. Design beautifully faster, smarter, and effortlessly.
              </div>
              <a href="mainModel" className="mt-10 inline-flex w-full items-center justify-center rounded-full border border-zinc-800/80 bg-[var(--color-bg)] px-8 py-5 font-serif tracking-wide text-zinc-900 transition-all duration-200 hover:-translate-y-0.5 hover:bg-[var(--color-secondary)] hover:text-white hover:shadow-lg focus:outline-none focus-visible:ring-2 focus-visible:ring-zinc-900/30 sm:w-auto md:text-3xl">try us now</a>
            </div>

            <div className="order-1 md:order-2">
              <div className="relative mx-auto w-full max-w-xl">
                <div className="overflow-hidden rounded-sm">
                  <img src={mainHomeImg} alt="Classic relief artwork" className="h-auto w-full object-cover" />
                </div>
                <div className="absolute right-[-8%] top-[50%] w-[38%] shadow-xl hidden xl:block" aria-hidden="true">
                  <div className="overflow-hidden rounded-sm">
                    <img src={secondaryHomeImg} alt="Marble sculpture" className="h-auto w-full object-cover" />
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>
    );
  }

  // Ready: mount motion elements with a key so initial -> animate runs
  return (
    <section className="bg-[var(--color-bg)] space-12">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:py-16 md:py-20">
        <div className="grid items-center gap-10 md:grid-cols-2 lg:gap-16">
          <div className="order-2 md:order-1">
            <h1 className="text-[80px] leading-none tracking-wide sm:text-[72px] md:text-[92px]">Arcana</h1>
              <div className="mt-4 max-w-lg rounded p-4 text-zinc-800">
                Arcana is an AI-powered interior design platform that transforms any room photo or sketch into photorealistic, purchasable designs in seconds. Powered by Anthropic’s Claude multi-agent system and ControlNet, Arcana intelligently understands your style, optimizes layouts, and curates real furniture within your budget. Design beautifully faster, smarter, and effortlessly.
              </div>
            <a href="mainModel" className="mt-10 inline-flex w-full items-center justify-center rounded-full border border-zinc-800/80 bg-[var(--color-bg)] px-8 py-5 font-serif tracking-wide text-zinc-900 transition-all duration-200 hover:-translate-y-0.5 hover:bg-[var(--color-secondary)] hover:text-white hover:shadow-lg focus:outline-none focus-visible:ring-2 focus-visible:ring-zinc-900/30 sm:w-auto md:text-3xl">try us now</a>
          </div>

          <div className="order-1 md:order-2">
            <div className="relative mx-auto w-full max-w-xl">
              <motion.div key={`main-${shouldAnimate}`} className="overflow-hidden rounded-sm" {...mainAnim}>
                <img src={mainHomeImg} alt="Classic relief artwork" className="h-auto w-full object-cover" />
              </motion.div>

              <motion.div key={`inset-${shouldAnimate}`} className="absolute right-[-8%] top-[50%] w-[38%] shadow-xl hidden xl:block" aria-hidden="true" {...insetAnim}>
                <div className="overflow-hidden rounded-sm">
                  <img src={secondaryHomeImg} alt="Marble sculpture" className="h-auto w-full object-cover" />
                </div>
              </motion.div>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}
