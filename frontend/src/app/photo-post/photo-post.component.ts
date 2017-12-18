import { Component, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../models/user.service';

@Component({
  selector: 'app-photo-post',
  templateUrl: './photo-post.component.html',
  styleUrls: ['./photo-post.component.css']
})
export class PhotoPostComponent implements OnInit {
  @ViewChild('fileInput') fileInput;

  constructor(
    private router: Router,
    private userService: UserService
  ) { }

  ngOnInit() {
    this.userService.getUser().then(user => {
      if (user.today_write_count <= 0) {
        alert('Sorry. You ran out of today\'s write count. Please wait until tomorrow!');
        this.router.navigate(['/gallery']);
      }
    });
  }

  url: string;
  tag = '';
  
  readUrl(event:any) {
    if (event.target.files && event.target.files[0]) {
      var reader = new FileReader();

      reader.onload = (event:any) => {
        this.url = event.target.result;
      }

      reader.readAsDataURL(event.target.files[0]);
    }
  }

  private upload() {
    if (this.tag === '') {
      alert('Tag is empty. Please fill in tag!');
      return;
    }

    const fileBrowser = this.fileInput.nativeElement;

    if (fileBrowser.files && fileBrowser.files[0]) {
      let fileSize = fileBrowser.files[0].size;
      let splittedFileName = fileBrowser.files[0].name.split(".")
      let fileType = splittedFileName[splittedFileName.length - 1]

      if (fileSize >= 2097152) {
        alert('Image size exceeds 2MB');
        console.log("size limit");
        return;
      }

      const formData = new FormData();
      formData.append('author_id', sessionStorage.getItem('user_id'));
      formData.append('image', fileBrowser.files[0]);
      formData.append('tag', this.tag);
      const xhr = new XMLHttpRequest();
      xhr.open('POST', '//127.0.0.1:8000/api/photo/upload/', true);
      xhr.send(formData);

      sessionStorage.setItem('today_write_count', String(Number(sessionStorage.getItem('today_write_count')) - 1));
    } else {
      alert('The image field is empty. Please upload an image!');
      return;
    }

    this.router.navigate(['/gallery']);
  }
}
