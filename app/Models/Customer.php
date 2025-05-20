<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Customer extends Model
{
    protected $table = 'customers';
    protected $primaryKey = 'customer_id';

    protected $fillable = [
        'name', 'email', 'phone', 'billing_address', 'shipping_address',
        'credit_limit', 'is_active'
    ];

    public $timestamps = true;
}
