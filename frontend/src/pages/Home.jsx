import React from "react";

// import image
import mainHomeImg from "../assets/homePic.png"
import secondaryHomeImg from "../assets/secondaryHomePic.png"


export default function Home() {
  return (
    <section className="bg-[var(--color-bg)] space-12">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:py-16 md:py-20">
        <div className="grid items-center gap-10 md:grid-cols-2 lg:gap-16">
          {/* Left: Title, copy, CTA */}
          <div className="order-2 md:order-1">
          {/* Display title */}
            <h1 className="text-[80px] leading-none tracking-wide sm:text-[72px] md:text-[92px]">
              Arcana
            </h1>


            {/* Lead paragraph in a subtle framed box */}
            <p className="mt-4 max-w-lg rounded p-4 text-zinc-800">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            </p>


            {/* CTA button */}
            <a
            href="mainModel"
            className="mt-10 inline-flex w-full items-center justify-center rounded-full border border-zinc-800/80 bg-[var(--color-bg)] px-8 py-5 font-serif tracking-wide text-zinc-900 transition-all duration-200 hover:-translate-y-0.5 hover:bg-[var(--color-secondary)] hover:text-white hover:shadow-lg focus:outline-none focus-visible:ring-2 focus-visible:ring-zinc-900/30 sm:w-auto md:text-3xl"
            >
            try us now
            </a>
          </div>
        


          <div className="order-1 md:order-2">
            <div className="relative mx-auto w-full max-w-xl">
            {/* Main image */}
              <div className="overflow-hidden rounded-sm">
                
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                src={mainHomeImg}
                alt="Classic relief artwork"
                className="h-auto w-full object-cover"
                />
                
              </div>

            {/* Inset overlapping image */}
            <div className="absolute right-[-8%] top-[50%] w-[38%] shadow-xl hidden xl:block" aria-hidden="true">
              <div className="overflow-hidden rounded-sm ">
            
                {/* // eslint-disable-next-line @next/next/no-img-element */}
                <img
                src={secondaryHomeImg}
                alt="Marble sculpture"
                className="h-auto w-full object-cover"
                />
              </div>
            </div>

            </div>
          </div>
        </div>
      </div>
    </section>
  );
}