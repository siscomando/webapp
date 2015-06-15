# lp-two-img-section

A element to create two columns content with image and text/legend below that 
very common in vast majority of the landing pages.

Usage
=====
The class `title`, `content-description` and `content-img` are required
to compose this presentation.

In this sample I used images (sprited) sized width="145" height="144".

```
<lp-lp-two-img-section minHeight="500" bgcolor="#F9F9F9" titlecolor="#979797">
      <span class="title">
      Art, Education & Social 
      </span>
      <div class="content-description">
        <p>Content description here...</p>        
      </div>
      <div class="content-img">
          <img-sprite src="/images/sprite-call.png" width="145" height="144"></img-sprite>
      </div>            
</lp-lp-two-img-section>
```
