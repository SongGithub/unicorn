#!/usr/bin/env python3

import json
from urllib import request
from urllib.error import HTTPError

import socket, ssl, datetime


def sort_list(l):
    """Takes a list and returns a sorted version"""
    # Assumption1: input list contains either numbers or char, not the two mixed.
    # Assumption2: input char has initial letters capitalized, while other letters in lower case.
    # ref: http://quiz.geeksforgeeks.org/merge-sort/
    left = 0
    right = len(l)-1
    sort_list_mergesort(l,left,right)
    return l


def sort_list_merge(arr,left,mid,right):
    """helper utility for the sort_list function to execute a merge"""

    n1 = mid - left + 1
    n2 = right - mid
    left_list = [None for _ in range(n1)] # create temp arrays
    right_list = [None for _ in range(n2)]

    for i in range(n1): # copy data to temp array
        left_list[i] = arr[left + i]

    for j in range(n2):
        right_list[j] = arr[mid + 1 + j]

    i = j = 0
    k = left
    while i < n1 and j < n2:  # compares the elements of two sub arrays and merge back to original array
        if left_list[i] <= right_list[j]:
            arr[k] = left_list[i]
            i += 1
        else:
            arr[k] = right_list[j]
            j += 1
        k += 1

    while i < n1: # copies the remaining elements of the left_list, if any
        arr[k] = left_list[i]
        i += 1
        k += 1

    while j < n2:
        arr[k] = right_list[j]
        j += 1
        k += 1


def sort_list_mergesort(l,left,right):
    """helper utility for the sort_list function to execute a merging-sort"""

    if left < right:
        mid = int(left + (right - left) / 2)

        sort_list_mergesort(l, left, mid)
        sort_list_mergesort(l, mid+1, right)

        sort_list_merge(l, left, mid, right)


def rgb_to_hex(red, green, blue):
    """
    Convert red, green, blue values into a HTML hex representation

    The short syntax should (#fff) be used where possible.
    """
    hex_list = ['{0:02x}'.format(red),'{0:02x}'.format(green),'{0:02x}'.format(blue)]

    short_syntax_list = []
    for colour in hex_list:
        if colour[0] == colour[1]:
            short_syntax_list.append(colour[0])
        else:
            break

    if len(short_syntax_list) == len(hex_list):
        # reset the Array 'list' when all 3 colours can be shortened.
        hex_list = short_syntax_list

    return '#{}{}{}'.format(hex_list[0],hex_list[1],hex_list[2])


def get_github_members(org_name):
    """
    Get the number of (public) members belonging to the specified Github
    organisation
    """

    """Challenge Met: github has pagination limit of 30, and absolute upper limit of 100.
    While real result > 150"""
    github_default_pagination = 30
    total_count = 0
    page = 1
    while True:
        url = "https://api.github.com/orgs/" + org_name + "/public_members?page=" + str(page)
        try:
            url_open = request.urlopen(url)
            response = ""

            while True:
                data = url_open.read().decode('utf-8')
                # print(data)
                if len(data) == 0:
                    break
                response += data

            json_data = json.loads(response)
            obj_count = len(json_data)
            total_count += obj_count
            page += 1
            if obj_count < github_default_pagination:
                break
        # return len(json_data)
        except HTTPError as e:
            print("HTTPError: github has a 'RateLimit' per IP address. Once exceeded, "
                  "there will be a 403 error returned.")
            break

    return total_count


def get_ssl_expiry(domain):
    """
    Takes a domain and returns a date that represents when the SSL certificate
    will expire.
    """
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=domain,
    )
    conn.settimeout(3.0)
    conn.connect((domain, 443))
    ssl_info = conn.getpeercert()
    conn.close()
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt).date()
