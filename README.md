# `buname`

`uname(1)`, but what if Linus Torvalds didn't hate large numbers

```console
$ uname -a
Linux sakuya 6.16.7 #1-NixOS SMP PREEMPT_DYNAMIC Thu Sep 11 15:23:23 UTC 2025 x86_64 GNU/Linux
$ buname -a
Linux sakuya 2.6.117.7 #1-NixOS SMP PREEMPT_DYNAMIC Thu Sep 11 15:23:23 UTC 2025 x86_64 GNU/Linux
$ buname -r
2.6.117.7
```

## What does the number mean?

> I decided to just bite the bullet, and call the next version 3.0. It
> will get released close enough to the 20-year mark, which is excuse
> enough for me, although honestly, the real reason is just that I can
> no [longer comfortably] count as high as 40.
>
> -- Linus Torvalds ([link](https://lore.kernel.org/lkml/BANLkTinE8eSSovGx6CPPkTeCpqv8AsS2nw@mail.gmail.com))

But what if we kept counting to 2.6.40 and beyond instead?

## The name "`buname`"

It stands for "big `uname`". You know, `uname(1)`, but with big numbers.
